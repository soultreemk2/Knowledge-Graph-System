#### 출처: https://docs.ampligraph.org/en/1.3.2/index.html ####


import numpy as np
import pandas as pd
import ampligraph
import tensorflow as tf

import requests
from ampligraph.datasets import load_from_csv
from ampligraph.evaluation import train_test_split_no_unseen 
from ampligraph.latent_features import save_model, restore_model

from ampligraph.evaluation import evaluate_performance, filter_unseen_entities
from ampligraph.evaluation import mr_score, mrr_score, hits_at_n_score
from scipy.special import expit

from ampligraph.discovery import discover_facts
from ampligraph.discovery import query_topn


#### 1. 데이터셋 불러오기 <s,r,o>

path = 'C:/Users/yangjh3/Desktop/업무폴더/Knowlege_Graph/예시데이터/'

data_total = pd.read_csv(path + '주간보고_SRO추출.csv', encoding='cp949')
data_total = data_total[['subject','relation','object']]
X = np.array(data_total, dtype='object')

entities = np.unique(np.concatenate([X[:, 0], X[:, 2]]))
relations = np.unique(X[:, 1])

Defining train and test datasets

num_test = int(len(X) * 0.04)

data = {}
data['train'], data['test'] = train_test_split_no_unseen(X, test_size=num_test, seed=0, allow_duplication=False) 


#### 2. Training Model
from ampligraph.latent_features import ComplEx
model = ComplEx(batches_count=100, 
                seed=0, 
                epochs=200, 
                k=150, 
                eta=5,
                optimizer='adam', 
                optimizer_params={'lr':1e-3},
                loss='multiclass_nll', 
                regularizer='LP', 
                regularizer_params={'p':3, 'lambda':1e-5}, 
                verbose=True)
positives_filter = X

## fitting the model
tf.logging.set_verbosity(tf.logging.ERROR)
model.fit(data['train'], early_stopping = False)
save_model(model, './best_model.pkl')


#### 3. Evaluation model

ranks = evaluate_performance(data['test'], 
                             model=model, 
                             filter_triples=positives_filter,   # Corruption strategy filter defined above 
                             use_default_protocol=True, # corrupt subj and obj separately while evaluating
                             verbose=True)


mrr = mrr_score(ranks)
print("MRR: %.2f" % (mrr))

hits_10 = hits_at_n_score(ranks, n=10)
print("Hits@10: %.2f" % (hits_10))
hits_3 = hits_at_n_score(ranks, n=3)
print("Hits@3: %.2f" % (hits_3))
hits_1 = hits_at_n_score(ranks, n=1)
print("Hits@1: %.2f" % (hits_1))


#### Hyper-parameter tuning ####

from ampligraph.evaluation import select_best_model_ranking

X_train_valid, X_test = train_test_split_no_unseen(X, test_size=2)
X_train, X_valid = train_test_split_no_unseen(X_train_valid, test_size=2)

param_grid = {
 "batches_count": [50],
 "seed": 0,
 "epochs": [100],
 "k": [100, 200],
 "eta": [5, 10, 15],
 "loss": ["pairwise", "nll"],
 "loss_params": {
     "margin": [2]
 },
 "embedding_model_params": {
 },
 "regularizer": ["LP", None],
 "regularizer_params": {
     "p": [1, 3],
     "lambda": [1e-4, 1e-5]
 },
 "optimizer": ["adagrad", "adam"],
 "optimizer_params": {
     "lr": lambda: np.random.uniform(0.0001, 0.01)
 },
 "verbose": False
}

select_best_model_ranking(ComplEx, X_train, X_valid, X_test, param_grid, max_combinations=100, use_filter=True, verbose=True,early_stopping=True) 


#### 4. Predicting New Links ####

### training set에는 없는 s,r,o

X_unseen = np.array([
    ['Jorah Mormont', 'SPOUSE', 'Daenerys Targaryen'],
])

unseen_filter = np.array(list({tuple(i) for i in np.vstack((positives_filter, X_unseen))}))

ranks_unseen = evaluate_performance(
    X_unseen, 
    model=model, 
    filter_triples=unseen_filter,   # Corruption strategy filter defined above 
    corrupt_side = 's+o',
    use_default_protocol=False, # corrupt subj and obj separately while evaluating
    verbose=True
)
ranks_unseen = evaluate_performance(
    X_unseen, 
    model=model, 
    filter_triples=unseen_filter,   # Corruption strategy filter defined above 
    corrupt_side = 's+o',
    use_default_protocol=False, # corrupt subj and obj separately while evaluating
    verbose=True
)
scores = model.predict(X_unseen)
probs = expit(scores)


#### 5 Discover New Facts ####

positives_filter = X
X_filtered = filter_unseen_entities(X, model)

target = ['개선']
new1 = discover_facts(X, model, strategy='entity_frequency', max_candidates=1000, target_rel=target, seed=0)


data_new1 = pd.DataFrame(new1[0])
data_new1.rename(columns = {0:'subject', 1:'relation', 2:'object'}, inplace = True)


new3 = query_topn(model, top_n=5, head='반맵', relation='유발', tail=None, ents_to_consider=None, rels_to_consider=None)
data_new3 = pd.DataFrame(new3[0])
data_new3.rename(columns = {0:'subject', 1:'relation', 2:'object'}, inplace = True)

