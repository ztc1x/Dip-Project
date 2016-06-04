import numpy as np
from sklearn import svm
from sklearn import cross_validation
from sklearn.metrics import accuracy_score
import cPickle
import pickle


def trainSVM(X, y, X_test, cv):
    model = svm.LinearSVC(C=0.1, dual=False) 
    print model
    
    scores = cross_validation.cross_val_score(model, X, y, cv=cv)
    print("%d-Fold Cross Validatoin Accuracy: %0.3f (+/- %0.3f)" % (cv, scores.mean(), scores.std() * 2))
    
    model.fit(X, y)  
    print 'Training Accuracy: %f' % accuracy_score(y, model.predict(X))
    y_pred = model.predict(X_test)
       
    return model, y_pred
   
    
if __name__ == '__main__':
    X_trainval = cPickle.load(open('./features/trainval_features.cPickle', 'rb'))
    y_trainval = np.load('./features/trainval_labels.cPickle')
    X_test = cPickle.load(open('./features/test_features.cPickle', 'rb'))
    
    model, y_pred = trainSVM(X_trainval, y_trainval, X_test, 4)
    oup = open('predictions.txt', 'wt')
    for label in y_pred:
        oup.write('0\n' if label == -1 else '1\n')
    oup.close()
    print 'predictions saved to ./predictions.txt'
    
    pickle.dump(model, open('model.pickle', 'wb'))
    print 'model saved to ./model.pickle'
    
