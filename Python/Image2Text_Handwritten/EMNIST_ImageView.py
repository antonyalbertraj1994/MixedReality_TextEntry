
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file into a pandas DataFrame
train_data = pd.read_csv(r"C:\Users\antony.irudayaraj\Downloads\archive\emnist-letters-train.csv")
test_data = pd.read_csv(r"C:\Users\antony.irudayaraj\Downloads\archive\emnist-letters-test.csv")


# Split the data into y_train and x_train
y_train = train_data.iloc[:, 0].values  # First column as y_train
x_train = train_data.iloc[:, 1:].values  # Remaining columns as x_train

y_test = test_data.iloc[:, 0].values
x_test = test_data.iloc[:, 1:].values



num_samples = 5  # Number of samples you want to visualize

fig, axes = plt.subplots(1, num_samples, figsize=(15, 5))

for i in range(num_samples):
    offset = 100
    ax = axes[i]
    print(np.shape(x_train[i + offset]))
    x_image = x_train[i + offset].reshape(28,28)
    ax.imshow(x_image, cmap='gray')  # Display the image in grayscale
    ax.set_title(f"Label: {chr(y_train[i + offset] + 96)}")  # Convert label to letter (1 -> 'a', 26 -> 'z')
    ax.axis('off')  # Hide the axis for clarity

plt.show()