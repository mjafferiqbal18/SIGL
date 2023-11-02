from spektral.layers import GeneralConv,GraphSageConv
from keras.layers import Dense
from keras.optimizers import Adam
from keras.losses import MeanSquaredError
from keras import  Model
import tensorflow as tf
from SIGL.Autoencoder.createSpekralGraphs import getGraphs


def autoencoder():

    graphs = getGraphs()
    epochs = 20
    loss_fn = MeanSquaredError()
    optimizer = Adam(learning_rate=0.001)

    #Define the autoencoder model
    class NN(Model):
        def __init__(self):
            super().__init__()
            self.conv1 = GraphSageConv(64, activation="relu")
            self.conv2 = GraphSageConv(32, activation="relu")
            self.dense = Dense(64, activation="relu")
            self.dense2  = Dense(128, activation='relu')

        def call(self, inputs):
            x, a = inputs
            x = self.conv1([x, a])
            x = self.conv2([x, a])
            x = self.dense(x)
            output = self.dense2(x)
            return output
        

    auto = NN()

    # Train to reduce reconstruction error
    
    @tf.function(reduce_retracing=True)
    def train(inputs,target):
        with tf.GradientTape() as tape:
            predictions = auto([inputs,target], training=True)
            loss = loss_fn(inputs, predictions)
            #loss += sum(auto.losses)
        gradients = tape.gradient(loss, auto.trainable_variables)
        optimizer.apply_gradients(zip(gradients, auto.trainable_variables))
        return loss


    for epoch in range(epochs):
        epoch_loss = 0.0

        for emb,adj in graphs:
            batch_loss = train(emb,adj)
        epoch_loss += batch_loss

        avg_epoch_loss = epoch_loss 
        print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_epoch_loss:.4f}")

    

    auto.save("auto")
    

