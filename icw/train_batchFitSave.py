from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Custom code
import classify_model as modelConfiguration
import train_datasetLoader as datasetLoader
import console_argv


trainDir, testDir = console_argv.getX(sys.argv, 2, 'trainDir testDir')

checkpoint_dir = os.path.dirname(modelConfiguration.checkpoint_path)

# Create checkpoint callback
cp_callback = keras.callbacks.ModelCheckpoint(modelConfiguration.checkpoint_path, 
                                                 save_weights_only=True,
                                                 verbose=1)

model = modelConfiguration.createModel()

data = datasetLoader.DataDict(trainDir,testDir)

batchSize = 125

# Trains the model using all training images in batches
model.fit_generator(datasetLoader.imageLoader(data.allTrainPaths,data.allTrainLabels,batchSize),steps_per_epoch=steps, epochs=5, callbacks=[cp_callback])

# Evaluates the whole range of test data to evaluate success
test_loss, test_acc = model.evaluate(datasetLoader.getImages(data.allTestPaths), data.allTestLabels)
print('Test accuracy:', test_acc)