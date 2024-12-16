from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import cv2 as cv
# Load the saved model
model = load_model('emnist_letters_model.keras')
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
dict_word = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M',
             13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y',
             25: 'Z'}

# Preprocess an image for prediction
def preprocess_image(image_path):
    # img = Image.open(image_path).convert('L')  # Convert to grayscale
    # img = img.resize((28, 28))  # Resize to 28x28
    # x_image = img.reshape(28, 28)
    #
    # img_array = np.expand_dims(x_image, axis=-1)  # Add channel dimension
    # img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    # img_array = np.array(img_array).astype('float32') / 255.0  # Normalize

    image1 = cv.imread(image_path)
    gray1 = cv.cvtColor(image1, cv.COLOR_BGR2GRAY)
    gray1 = cv.rotate(gray1, cv.ROTATE_90_COUNTERCLOCKWISE)
    #gray = cv.medianBlur(gray, 5)

    #element = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    #gray1 = cv.morphologyEx(gray1, cv.MORPH_GRADIENT, element)

    gray1 = cv.resize(gray1, (28, 28), interpolation=cv.INTER_AREA)  # resizing
    ret, gray1 = cv.threshold(gray1, 100, 255, cv.THRESH_BINARY)

    # reshaping the image
    gray1 = np.reshape(gray1, (28, 28))
    cv.imshow("image", gray1)
    cv.waitKey(0)

    img_array1 = np.expand_dims(gray1, axis=-1)  # Add channel dimension
    img_array2 = np.expand_dims(img_array1, axis=0)  # Add batch dimension
    img_array3 = img_array2.astype('float32') / 255.0  # downsampling

    return img_array3

# Predict on a new image

# Load the CSV file into a pandas DataFrame
train_data = pd.read_csv(r"C:\Users\antony.irudayaraj\Downloads\archive\emnist-letters-train.csv")
test_data = pd.read_csv(r"C:\Users\antony.irudayaraj\Downloads\archive\emnist-letters-test.csv")


# Split the data into y_train and x_train
y_train = train_data.iloc[:, 0].values  # First column as y_train
x_train = train_data.iloc[:, 1:].values  # Remaining columns as x_train

y_test = test_data.iloc[:, 0].values
x_test = test_data.iloc[:, 1:].values

sampleno = 4500

image_path = r"C:\Users\antony.irudayaraj\Desktop\VRTextEntry\Character_Images\drawing.jpg"
image = cv.imread(image_path)
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
# gray = cv.medianBlur(gray, 5)
# element = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
# gray = cv.morphologyEx(gray, cv.MORPH_GRADIENT, element)
gray = cv.resize(gray, (28, 28),interpolation=cv.INTER_AREA)  # resizing
ret, gray = cv.threshold(gray, 10, 255, cv.THRESH_BINARY_INV)
gray = np.reshape(gray, (28, 28))
#gray = np.expand_dims(gray, axis=-1)  # Add channel dimension



x_sample = x_test[sampleno]
actual_y = y_test[sampleno]
print("Actual Symbol", actual_y)

fig, axes = plt.subplots(1, 2, figsize=(15, 5))
ax = axes[0]
x_image = x_sample.reshape(28, 28)
img_array = np.expand_dims(x_image, axis=-1)  # Add channel dimension

ax.imshow(x_image, cmap='gray')  # Display the image in grayscale
ax.set_title(str(dict_word[actual_y - 1]))
plt.show()

img_array = np.expand_dims(img_array, axis=0)  # Add channel dimension
img_array = img_array.astype('float32') / 255.0


image_path = r"C:\Users\antony.irudayaraj\Desktop\VRTextEntry\Character_Images\drawing.jpg"
input_image = preprocess_image(image_path)
prediction = model.predict(input_image)
predicted_class = np.argmax(prediction)   # Add 1 to match original labels (1-26)


print(dict_word[predicted_class])