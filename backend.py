import pandas as pd
import numpy as np
import pickle
# from sklearn.preprocessing import StandardScalar
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from KNN_class import KNN
from sklearn.neighbors import KNeighborsClassifier
diabetic_data= pd.read_csv("diabetes.csv")
print(diabetic_data.head())
X= diabetic_data.iloc[:,:8]
y= diabetic_data.iloc[:,-1]
# print(X)
# print(y)
# n= np.sqrt(len(diabetic_data))
# print(n)

X_train,X_test,y_train,y_test= train_test_split(X,y,test_size=0.3)
# print(X_train)
# print(X_test)
# print("=======================================================")
# print(np.array(X_test))
# print("=======================================================")
# for x in np.array(X_test):
#     print(x)


clf= KNN(k=5)
model= clf.fit(X_train,y_train)
predictions= clf.predict1(X_test)
print(predictions)
print("=======================================================")
acc= accuracy_score(y_test,predictions)
print(acc)
print("=======================================================")
f1_score_1= f1_score(y_test,predictions)
print(f1_score_1)
print("=======================================================")
cm_1= confusion_matrix(y_test,predictions)
print(cm_1)
# for i in range(0,len(X)):
#     print(type(X.iloc[i,:]))
print("================================================")
# print("KNN inbuild module")

# model_KNN= KNeighborsClassifier(n_neighbors=5)
# model_KNN_fit= model_KNN.fit(X_train,y_train)
# pred= model_KNN_fit.predict(X_test)
# print("=======================================================")
# print(pred)
# acc_lib= accuracy_score(y_test,pred)
# print("=======================================================")
# print(acc_lib)
# print("=======================================================")
# f1_score_lib= f1_score(y_test,pred)
# print(f1_score_lib)
# print("=======================================================")
# cm_lib= confusion_matrix(y_test,pred)
# print(cm_lib)
pickle_model_path='KNN_model.pkl'
with open (pickle_model_path,'wb') as f:
  pickle.dump(clf,f)