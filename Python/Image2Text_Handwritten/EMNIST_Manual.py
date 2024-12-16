import numpy as np
import struct
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import SGD


# Function to load IDX files (same as before)
def load_idx(file_path):
    with open(file_path, 'rb') as f:
        magic, size = struct.unpack('>II', f.read(8))
        if magic == 2051:  # If images
            rows, cols = struct.unpack('>II', f.read(8))
            data = np.frombuffer(f.read(), dtype=np.uint8).reshape(size, rows, cols)
        elif magic == 2049:  # If labels
            data = np.frombuffer(f.read(), dtype=np.uint8)
        else:
            raise ValueError("Invalid magic number in IDX file")
    return data

# Paths to the EMNIST letters dataset files (update the paths accordingly)
import pandas as pd

import pandas as pd

# Load the CSV file into a pandas DataFrame
train_data = pd.read_csv(r"C:\Users\antony.irudayaraj\Downloads\archive\emnist-letters-train.csv")
test_data = pd.read_csv(r"C:\Users\antony.irudayaraj\Downloads\archive\emnist-letters-test.csv")


# Split the data into y_train and x_train
y_train = train_data.iloc[:, 0].values  # First column as y_train
x_train = train_data.iloc[:, 1:].values  # Remaining columns as x_train

y_test = test_data.iloc[:, 0].values
x_test = test_data.iloc[:, 1:].values


# Preprocess the data
x_train = x_train.astype('float32') / 255.0  # Normalize pixel values to [0, 1]
x_test = x_test.astype('float32') / 255.0
print("max", np.max(x_train), np.max(x_test))
x_train = np.expand_dims(x_train, axis=-1)  # Add channel dimension
x_test = np.expand_dims(x_test, axis=-1)

x_train = x_train.reshape(-1, 28, 28, 1)
x_test = x_test.reshape(-1, 28, 28, 1)

print("x_train", x_train.shape, y_train.shape)
print("test data", x_test.shape, y_test.shape)

#x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255.0  # Normalize and reshape
#x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255.0

# x_train = np.expand_dims(x_train, axis=-1)  # Add channel dimension
# x_test = np.expand_dims(x_test, axis=-1)

# Adjust labels (EMNIST letters are labeled 1-26; shift to 0-25 for categorical classification)
y_train = y_train - 1  # EMNIST labels start from 1 (a=1, ..., z=26)
y_test = y_test - 1
num_classes = 26  # There are 26 lowercase letters (a-z)

# Convert labels to one-hot encoding
y_train = tf.keras.utils.to_categorical(y_train, num_classes)
y_test = tf.keras.utils.to_categorical(y_test, num_classes)

# Verify the shapes
print(f"x_train shape: {x_train.shape}, y_train shape: {y_train.shape}")
print(f"x_test shape: {x_test.shape}, y_test shape: {y_test.shape}")


# Build the CNN model
model = Sequential([
    # Convolutional Layer 1: 32 filters, 3x3 kernel, ReLU activation
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),  # MaxPooling layer with 2x2 pool size

    # Convolutional Layer 2: 64 filters, 3x3 kernel, ReLU activation
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),

    # Convolutional Layer 3: 128 filters, 3x3 kernel, ReLU activation
    Conv2D(128, (3, 3), activation='relu'),

    # Flatten layer to convert 3D tensor to 1D vector
    Flatten(),

    # Fully Connected Layer with 128 units and ReLU activation
    Dense(128, activation='relu'),

    # Output layer with 26 units (for 26 letters), using softmax for multi-class classification
    Dense(26, activation='softmax')
])

optimizer = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)

# Compile the model
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

#model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])


# Train the model
history = model.fit(
    x_train, y_train,
    epochs=50,
    batch_size=128,
    validation_data=(x_test, y_test)
)

# Evaluate the model
test_loss, test_accuracy = model.evaluate(x_test, y_test)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

# Save the model
model.save('emnist_letters_model_sgd.keras')
print("Model saved as 'emnist_letters_model.h5'")

print(model.summary())
