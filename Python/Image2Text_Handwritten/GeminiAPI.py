import google.generativeai as genai
from PIL import Image
import time

def process(filelocation):
    genai.configure(api_key='AIzaSyD1YyuLBOAPEAxcPfsl49JPFpI0M5k8H3c')
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')

    # result = model.generate_content("What is the sum of the first 50 prime numbers?"
    #                                 "Generate and run code for the calculation, and make sure you get all 50.")
    time1 = time.time()
    image = Image.open(filelocation)
    #image = Image.open(r'C:\Users\antony.irudayaraj\Desktop\VRTextEntry\Character_Images\S.jpg')
    prompt = "Important: Only return a single english alphabet. Only a single character and nothing else. \n It is not a number."

    result_image = model.generate_content([image, prompt])
    print("image_result", result_image.text)
    time2 = time.time()
    print("time elapsed", time2 - time1)

# for part in result.candidates[0].content.parts:
#   print(part)
#   print()
process(r'C:\Users\antony.irudayaraj\Desktop\VRTextEntry\Character_Images\AndroidImported\canvas_image_S_edited.png')