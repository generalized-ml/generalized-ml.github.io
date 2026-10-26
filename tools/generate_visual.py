"""Generate an offline interactive 3D visual. Run from any directory with Python 3."""

# lets create a visuals for gradient descent for a loss function 

#lets first define the dataset X,Y from sklearn.datasets import make_moons
from sklearn.datasets import make_moons
X, Y = make_moons(n_samples=200, noise=0.3, random_state=42)
#lets create a neural network with 2 hidden layers and 10 neurons in each layer
import numpy as np
#lets save the gradients in a list for each epoch

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.W1 = np.random.randn(input_size, hidden_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size)
        self.b2 = np.zeros((1, output_size))
    def forward(self, X):
        self.Z1 = np.dot(X, self.W1) + self.b1
        self.A1 = self.sigmoid(self.Z1)
        self.Z2 = np.dot(self.A1, self.W2) + self.b2
        self.A2 = self.sigmoid(self.Z2)
        return self.A2
    def backward(self, X, Y, output):
        m = Y.shape[0]
        dZ2 = output - Y
        dW2 = np.dot(self.A1.T, dZ2) / m
        db2 = np.sum(dZ2, axis=0, keepdims=True) / m
        dZ1 = np.dot(dZ2, self.W2.T) * self.sigmoid_derivative(self.Z1)
        dW1 = np.dot(X.T, dZ1) / m
        db1 = np.sum(dZ1, axis=0, keepdims=True) / m
        return dW1, db1, dW2, db2
    def update_parameters(self, dW1, db1, dW2, db2, learning_rate):
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
    def sigmoid(self, Z):
        return 1 / (1 + np.exp(-Z))
    def sigmoid_derivative(self, Z):
        return Z * (1 - Z)


#lets fit the neural network to the dataset and save the gradients for each epoch keep the network small so that we can visualize the gradients in 3D
nn = NeuralNetwork(input_size=2, hidden_size=10, output_size=1)
gradients = []
for epoch in range(1000):
    output = nn.forward(X)
    
    #save the gradients for each epoch lets save the Weights and biases gradients as well as the epoch number in a list of lists

    dW1, db1, dW2, db2 = nn.backward(X, Y.reshape(-1, 1), output)
    W1_norm = np.linalg.norm(nn.W1)
    W2_norm = np.linalg.norm(nn.W2)
    loss = np.mean((output - Y.reshape(-1, 1)) ** 2)
    gradients.append([epoch, dW1, db1, dW2, db2, W1_norm, W2_norm, loss])
    nn.update_parameters(dW1, db1, dW2, db2, learning_rate=0.01)


#lets plot the gradients in 3D using plotly
#import plotly and use plotly to visualize the gradients in 3D


import plotly.graph_objects as go
#lets take two gradients dW1 and dW2 and plot them in 3D with epoch on the x-axis, dW1 on the y-axis and dW2 on the z-axis
epochs = [g[0] for g in gradients]
dW1 = [np.linalg.norm(g[1]) for g in gradients]
dW2 = [np.linalg.norm(g[3]) for g in gradients]
W1_norm = [g[5] for g in gradients]
W2_norm = [g[6] for g in gradients]
loss = [g[7] for g in gradients]
#lets create a 3D plot with onw axis as loss function one axis W1 and one axis W2 and color the points by epoch
print("Creating 3D plot...")
#also show gradients as arrows in the 3D plot
fig = go.Figure(data=[go.Scatter3d(
    x=loss,
    y=W1_norm,
    z=W2_norm,
    mode='markers',
    marker=dict(
        size=5,
        color=epochs,                # set color to an array/list of desired values
        colorscale='Viridis',   # choose a colorscale
        opacity=0.8
    )
)])
#add arrows to the plot to show the gradients
for i in range(len(epochs)):
    fig.add_trace(go.Cone(
        x=[loss[i]],
        y=[W1_norm[i]],
        z=[W2_norm[i]],
        u=[dW1[i]],
        v=[dW2[i]],
        w=[0],
        sizemode="absolute",
        sizeref=0.1,
        anchor="tail",
        showscale=False
    ))
fig.update_layout(
    scene=dict(
        xaxis_title='Loss',
        yaxis_title='||W1||',
        zaxis_title='||W2||'
    ),
    title='3D Visualization of Gradients during Training'
)
#save the plot as an html file
fig.write_html("gradients_3d_plot.html")    

