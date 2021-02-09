# CNN for device-free localization

import numpy as np
import tensorflow as tf
import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, Conv1D, MaxPooling2D
from keras import backend as K
import scipy.io # scipy.io.loadmat / savemat

dataset_filename   = 'clean_32pos.mat'
positions_filename = 'positions32.mat'

# Each file contains 3 matrices: training, testing, validation
csi = scipy.io.loadmat(dataset_filename)
positions = scipy.io.loadmat(positions_filename)

# Each csi matrix has size: L x M x N, where
#  L = (no. of samples per positions) x (no. of positions)
#  M = 234 = no. of active OFDM subcarriers
#  N = 8   = (Real and Imaginary parts) x (no. of antennas)
training_set   = csi['training'].astype('float')
testing_set    = csi['testing'].astype('float')
validation_set = csi['validation'].astype('float')

# Take only the first two elements of the csi, i.e. real and imag parts of antenna 1
antenna_select = [ [0,1], [2,3], [4,5], [6,7] ]
antenna = antenna_select[0]

training_set   = training_set[:,:,antenna]
testing_set    = testing_set[:,:,antenna]
validation_set = validation_set[:,:,antenna]

# Normalize datasets using training data (which would be the only ones available offline)
maxval = np.max(training_set)
training_set   = training_set/maxval
testing_set    = testing_set/maxval
validation_set = validation_set/maxval

# Each positions matrix has size: L x O, where
#  L = (no. of samples per positions) x (no. of positions)
#  O = 2 (x-y coordinates)
training_positions = positions['training'].astype('float')
testing_positions  = positions['testing'].astype('float')
# validation data in our case have the same size of testing

# Double-check that all sizes are coherent
print('  Training set size =', training_set.shape)
print('   Testing set size =', testing_set.shape)
print('Validation set size =', validation_set.shape)
print('---------------------------------------------')
print('  Training set size =', training_positions.shape)
print('   Testing set size =', testing_positions.shape)
print('Validation set size =', testing_positions.shape) # validation size = testing size

def lrscore(y_true, y_pred):
    R = tf.constant(0.3)
    distances = K.sqrt(K.sum(K.square(y_pred - y_true),axis=1))
    insideR3 = tf.math.reduce_sum(tf.cast(tf.math.less(distances,3*R), tf.float32))
    insideR2 = tf.math.reduce_sum(tf.cast(tf.math.less(distances,2*R), tf.float32))
    insideR1 = tf.math.reduce_sum(tf.cast(tf.math.less(distances,1*R), tf.float32))
    tensor_size = tf.cast(tf.size(y_pred), tf.float32)/2.0
    return (insideR1*0.50 + insideR2*0.25 + insideR3*0.25)/tensor_size

# Define an early stopping policy
earlystopping_cb = tf.keras.callbacks.EarlyStopping(monitor='val_lrscore',patience=4,mode='max')

num_neurons_first_layer = training_set.shape[1:]

model_name = 'mymodel'
print(model_name)

model = Sequential()
model.add(Conv1D(30, 5, padding='same', activation='relu', input_shape=num_neurons_first_layer))
model.add(Conv1D(50, 5, padding='same', activation='relu'))
model.add(Flatten())
model.add(Dense(100, activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(2))

model.compile(loss="mean_squared_error", optimizer="adam", metrics=[lrscore])
model.summary()

history = model.fit(
    training_set, training_positions,
    batch_size=300, epochs=100, shuffle=True,
    validation_data=(validation_set,testing_positions),
    callbacks=[earlystopping_cb]);

model.save(model_name);

loss_name = model_name + 'loss.txt'
perf_name = model_name + 'metric.txt'

loss_history = history.history["val_loss"]
perf_history = history.history["val_lrscore"]

np_loss_history = np.array(loss_history)
np_perf_history = np.array(perf_history)

np.savetxt(loss_name, np_loss_history, delimiter=',')
np.savetxt(perf_name, np_perf_history, delimiter=',')

# Save a file with predictions
predictions = model.predict(testing_set, verbose=1)
scipy.io.savemat('predictions.mat', {'predictions': predictions})
