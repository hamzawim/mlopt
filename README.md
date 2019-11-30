[![Build Status](https://travis-ci.com/pklauke/mlopt.svg?branch=master)](https://travis-ci.com/pklauke/mlopt)

# mlopt

Python library including algorithms for optimization problems like weighted blending, hyperparameter tuning and more.

# Installation

The package can be downloaded using

        git clone https://github.com/pklauke/mlopt
        
Afterwards it can be installed with

        cd mlopt 
        python3 setup.py install

# Usage
Example for weighted blending with greedy optimization:

        from sklearn.metrics import mean_absolute_error
        from mlopt import BlendingTransformer

        labels = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        predictions_model_1 = [0.11, 0.19, 0.25, 0.37, 0.55, 0.62, 0.78, 0.81, 0.94]
        predictions_model_2 = [0.07, 0.21, 0.29, 0.33, 0.53, 0.54, 0.74, 0.74, 0.91]
        predictions_blended = [predictions_model_1, predictions_model_2]

        blender = BlendingTransformer(metric=mean_absolute_error, maximize=False)
        blender.fit(y=labels, X=predictions_blended)

        weights = blender.weights
        score = blender.score

        print('MAE 1: {:0.3f}'.format(mean_absolute_error(labels, predictions_model_1)))
        print('MAE 2: {:0.3f}'.format(mean_absolute_error(labels, predictions_model_2)))
        print('Optimized blending weights: ', weights)
        print('MAE blended: {:0.3f}'.format(score))
