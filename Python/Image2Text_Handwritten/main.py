# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import glob

from keras.models import load_model

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    model = load_model('best_model.h5')
    dict_word = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X', 24:'Y',25:'Z'}
    images = [cv.imread(file) for file in glob.glob(r"C:\Users\antony.irudayaraj\Desktop\VRTextEntry\Character_Images\*.jpg")]
    # fig, axes = plt.subplots(7, 4, figsize=(30, 30))
    # axes = axes.flatten()
    # for i in range(len(images)):
    #     axes[i].imshow(images[i])
    # plt.delaxes(ax=axes[26])
    # plt.delaxes(ax=axes[27])


    fig, axes = plt.subplots(7, 4, figsize=(30, 30))
    axes = axes.flatten()

    for i in range(len(images)):
        gray = cv.cvtColor(images[i], cv.COLOR_BGR2GRAY)
        gray = cv.medianBlur(gray, 5)
        ret, gray = cv.threshold(gray, 75, 255, cv.THRESH_BINARY)

        element = cv.getStructuringElement(cv.MORPH_RECT, (1, 1))
        gray = cv.morphologyEx(gray, cv.MORPH_GRADIENT, element)

        gray = gray / 255.  # downsampling
        # gray = 1 - gray
        gray = cv.resize(gray, (28, 28))  # resizing

        # reshaping the image
        gray = np.reshape(gray, (28, 28))

        axes[i].imshow(gray)

        pred = dict_word[np.argmax(model.predict(np.reshape(gray, (1, 28, 28, 1))))]
        axes[i].set_title("Prediction: " + pred, fontsize=30, fontweight='bold', color='green')
        plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)

    # removing the unnecessary subplots
    plt.delaxes(ax=axes[26])
    plt.delaxes(ax=axes[27])
    plt.show()



model = load_model('best_model.h5')

def process(image_filename):
    print("dfg")

    image = cv.imread(image_filename)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.medianBlur(gray, 5)
    gray = cv.resize(gray, (28, 28), interpolation=cv.INTER_AREA)  # resizing

    ret, gray = cv.threshold(gray, 20, 255, cv.THRESH_BINARY)

    element = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    gray = cv.morphologyEx(gray, cv.MORPH_GRADIENT, element)

    #cv.imshow("image", gray)
    #cv.waitKey(0)

    gray = gray / 255.  # downsampling
    # gray = 1 - gray

    # reshaping the image
    gray = np.reshape(gray, (28, 28))

    #axes[i].imshow(gray)
    dict_word = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X', 24:'Y',25:'Z'}
    pred = dict_word[np.argmax(model.predict(np.reshape(gray, (1, 28, 28, 1))))]
    print("Predict value", pred)
    return pred
    #axes[i].set_title("Prediction: " + pred, fontsize=30, fontweight='bold', color='green')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print_hi('PyCharm')
    process(r"C:\Users\antony.irudayaraj\Desktop\VRTextEntry\Character_Images\drawing.jpg")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
