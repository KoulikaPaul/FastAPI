import numpy as np
from collections import Counter
# def euclidean_distance(a,b):
#     #    print(type(a),type(b))
#     #    print("a", a)
#     #    print("b", b)

#        distance= np.sqrt(np.sum((a-b)**2))
#        return(distance)
class KNN:
    
    def __init__(self,k=3):
      self.k=k


    
    @staticmethod
    def euclidean_distance(a,b):
       print(type(a),type(b))
       print("a", a)
       print("b", b)

       distance= np.sqrt(np.sum((a-b)**2))
       return(distance)

    def fit(self,X,y):
       self.X_train=np.array(X)
       self.y_train=np.array(y)

    def predict1(self,X):
       X= np.array(X)
       predictions=([self.calculate(x) for x in X])
       return(predictions)   
    def calculate(self,x):
        distances=([KNN.euclidean_distance(x, x_train) for x_train in self.X_train ])
       
        k_neighbors_indices=np.argsort(distances)[:self.k]

        y_levels_k_neighbors= [self.y_train[i] for i in k_neighbors_indices]
        most_common_class= Counter(y_levels_k_neighbors).most_common()[0][0]
        return(most_common_class)