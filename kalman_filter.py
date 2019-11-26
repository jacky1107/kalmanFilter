import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle

def dot(p, *args):
    for arg in args:
        p = np.dot(p, arg)
    return p

def F(t):
    return np.array([[1, 0, t, 0],
                     [0, 1, 0, t],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1],])

def B(t):
    t_ = (t**2)/2
    return np.array([[t_, 0],
                     [0, t_],
                     [t, 0],
                     [0, t]])

def U(ax, ay):
    return np.array([[ax],
                     [ay]])

def inverse(array):
    return np.linalg.inv(array)

true = pickle.load(open("c_acceleration/true.pickle","rb"))
track1 = pickle.load(open("c_acceleration/track1.pickle","rb"))
track2 = pickle.load(open("c_acceleration/track2.pickle","rb"))
track3 = pickle.load(open("c_acceleration/track3.pickle","rb"))

# for observation position
Z = track2

# for F and B
t = 0.01

x_noise = np.random.normal(0, Z[:,0].std(), 200)
y_noise = np.random.normal(0, Z[:,1].std(), 200)
ax1, ay = 0,0#x_noise, y_noise
FT = F(t).transpose()

# for state X
x_position = true[0,0]
y_position = true[0,1]

X = np.zeros((4,1))
X_= np.zeros((4,1))

# for variance P
P = np.eye(4)
P[2,2] = 0
P[3,3] = 0

# for observation error
R = np.array([[(Z[:,0].std())**2, 0],
              [0, (Z[:,1].std())**2]])

# for noise
W = 1e-3

#processNoiseCov
Q = Z[:,0].std() * Z[:,1].std()

# for Identity Matrix
I = np.eye(4)
H = np.array([[1, 0, 0, 0],
              [0, 1, 0, 0]])
HT= H.transpose()


fig = plt.figure()
ax = fig.add_subplot(111)


kalmanX, kalmanY = [], []
var_err_X, var_err_Y = [], []
error_obv, error_kal = [], []
#==================================================================
# formula
for i in range(len(true)):
    X_= dot(F(t), X) + dot(B(t), U(ax1, ay)) + W
    
    P_= dot(F(t), P, FT) + Q
    
    P_= P_*I
    K = dot(dot(P_, HT), inverse(dot(H, P_, HT) + R))
    
    S = Z[i].reshape((2,1)) - dot(H, X_)

    X = X_ + dot(K, S)
    
    P = dot((I - dot(K, H)), P_)
    
    ax.scatter(X[0,0],X[1,0], c='g');plt.pause(t)
    ax.scatter(true[i,0],true[i,1], c='b');plt.pause(t)
    ax.scatter(Z[i,0],Z[i,1], c='orange');plt.pause(t)

    error_obv.append( (true[i,0]-Z[i,0])**2+(true[i,1]-Z[i,1])**2)
    error_kal.append( (true[i,0]-X[0,0])**2+(true[i,1]-X[1,0])**2)

    kalmanX.append(X[0,0])
    kalmanY.append(X[1,0])
    
    var_err_X.append(P[0,0])
    var_err_Y.append(P[1,1])

print("mean_square:")
print((sum(error_kal)/len(error_kal)) / (sum(error_obv)/len(error_obv)))
plt.show()
plt.plot(true[:,0],true[:,1])
plt.plot(Z[:,0],Z[:,1],c='orange')
plt.plot(kalmanX, kalmanY, c='g')
plt.show()

plt.plot(range(1,len(error_obv)*100,100), error_obv, c='orange')
plt.plot(range(1,len(error_kal)*100,100), error_kal, c='g')
plt.show()

plt.plot(range(len(var_err_X)), var_err_X, c='orange')
plt.plot(range(len(var_err_Y)), var_err_Y, c='g')
plt.show()

plt.plot(range(len(ay)), ax)
