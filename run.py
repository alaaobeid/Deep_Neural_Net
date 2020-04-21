# -*- coding: utf-8 -*-
"""neural_network.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SIE_KhCuHbwbK90PI33-E8xXgV3DGw0o
"""
from neural_network import *
from keras.datasets import mnist
from keras.utils import np_utils
import time
# loading MNIST from sklearn package
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.astype('float32')
x_train /= 255
y_train = np_utils.to_categorical(y_train)


x_test = x_test.astype('float32')
x_test /= 255
y_test = np_utils.to_categorical(y_test)
#Create the deep neural network as a list of layers
network = [
    FlattenLayer(input_shape=(28, 28)),
    FCLayer(28 * 28, 150),
    ActivationLayer(sigmoid, sigmoid_prime),
    FCLayer(150, 50),
    ActivationLayer(sigmoid, sigmoid_prime),
    FCLayer(50, 10),
    ActivationLayer(rectifier, rectifier_prime)
]

epochs = 10
learning_rate = 0.1

# training
for epoch in range(epochs):
    error = 0
    training = np.concatenate((x_train.reshape(60000,784), y_train), axis=1) 
    np.random.shuffle(training)
    x_train=training[0:,0:784].reshape(60000,28,28)
    y_train=training[:60000,784:]
    for x, y_true in zip(x_train, y_train):
        # forward
        output = x
        for layer in network:
            output = layer.forward(output)
        
        # error (display purpose only)
        error += mse(y_true, output)

        # backward
        output_error = mse_prime(y_true, output)
        for layer in reversed(network):
            output_error = layer.backward(output_error, learning_rate)
    
    error /= len(x_train)
    print('%d/%d, error=%f' % (epoch + 1, epochs, error))


#test the network and print a classification report
test_network(network,x_test,y_test)











import matplotlib.pyplot as plt
#iterate through the testing data and print the prediction with highest probability and the actual label
samples = 10
for test, true in zip(x_test[:samples], y_test[:samples]):
    print_digit(test)
    pred = predict(network, test)[0]
    idx = np.argmax(pred)
    idx_true = np.argmax(true)
    print('pred: %s, prob: %.2f, true: %d' % (idx, pred[idx], idx_true))
    time.sleep(0.2)
