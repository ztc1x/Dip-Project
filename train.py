import numpy as np
from sklearn import svm
from sklearn import cross_validation
from sklearn.metrics import accuracy_score
import cPickle

X_trainval = cPickle.load(open('./features/trainval_features.cPickle', 'rb'))
y_trainval = np.load('./features/trainval_labels.cPickle')

model = svm.LinearSVC(C=0.1, dual=False) 
print model
model.fit(X_trainval, y_trainval)

print 'Training Accuracy: %f' % accuracy_score(y_trainval, model.predict(X_trainval))
fold = 4
scores = cross_validation.cross_val_score(model, X_trainval, y_trainval, cv=fold)
print("%d-Fold Validatoin Accuracy: %0.3f (+/- %0.3f)" % (fold, scores.mean(), scores.std() * 2))