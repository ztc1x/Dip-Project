import numpy as np
from sklearn import svm
from sklearn import cross_validation
from sklearn.metrics import accuracy_score

X_trainval = np.load('./features/trainval_features.npy')
y_trainval = np.load('./features/trainval_labels.npy')

model = svm.LinearSVC(dual=False)
model.fit(X_trainval, y_trainval)
print model
print 'Training Accuracy: %f' % accuracy_score(y_trainval, model.predict(X_trainval))

fold = 3
scores = cross_validation.cross_val_score(model, X_trainval, y_trainval, cv=fold)
print("%d-Fold Validatoin Accuracy: %0.3f (+/- %0.3f)" % (fold, scores.mean(), scores.std() * 2))