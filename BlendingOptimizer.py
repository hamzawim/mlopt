import numpy as np

class BlendingOptimizer:
    maximize = True
    weights = []
    metric = None
    score = None
    
    def __init__(self, metric, maximize = True):    
        self.metric = metric
        self.maximize = maximize
        
    def is_better_score(self, score_to_test, score):
        cond = score_to_test > score
        return cond if self.maximize else not cond
        
    def fit(self, predictions, real, step = 0.1, init_weights = None, warm_start = False):
        if (init_weights != None) and warm_start:
            print('Warning: When warm_start is used init_weights are ignored.')
        
        assert(np.shape(predictions)[1] == len(real))
        
        le = len(predictions)
        
        if warm_start:
            weights = self.weights
        elif init_weights == None:
            weights = np.array([1.0] * le)
        else:
            assert(len(init_weights) == le)
            weights = init_weights

        score = 0
        best_score = score + self.maximize -0.5
        
        while self.is_better_score(best_score, score):
            best_score = self.metric(real, np.average(predictions, weights=weights, axis=0))
            score = best_score
            best_index, best_step = -1, 0.0
            for j in range(le):
                delta = np.array([(0 if k != j else step) for k in range(le)])
                s = self.metric(real, np.average(predictions, weights=weights+delta, axis=0))
                if self.is_better_score(s, best_score):
                    best_index, best_score, best_step = j, s, step
                    continue
                if weights[j] - step >= 0:
                    s = self.metric(real, np.average(predictions, weights=weights-delta, axis=0))
                    if(s > best_score):
                        best_index, best_score, best_step = j, s, -step
            if self.is_better_score(best_score, score):
                weights[best_index] += best_step
                
        self.weights = weights
        self.score = best_score
        return weights
    
    def predict(self, predictions):
        return np.average(predictions, weights = self.weights, axis = 0)