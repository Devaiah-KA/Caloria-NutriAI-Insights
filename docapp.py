from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt,image,input):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([prompt,image[0],input])
    return response.text




def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        #read the file into bytes
        bytes_data=uploaded_file.getvalue()
        
        #format req by geminiai
        image_parts=[
            {
                "mime_type": uploaded_file.type, #get typpe of file uploaded
                "data": bytes_data
            }  
        ]
        return image_parts
    else:
        raise FileNotFoundError("file not Uploaded")
    
    


#streamlit app
 
st.set_page_config(page_title="AI Calorie Doctor")
st.header("Gemini Health App")
input=st.text_input("Food Info(If required): ",key="input")
uploaded_file = st.file_uploader("Choose image...",type=["jpeg","jpg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Upload image.",use_column_width=True)
    
submit=st.button("Tell me about the total calories")

#prompt setup

prompt = """
The information about the food is given in the input.
You are an expert in nutritionist where you need to see the food items from the image
 and calculate the calories according to the grams.
The individual items should sum up to the total size of the food.Hence spilt the items
 according to their portion from the image and calculate for them individually.
 Also provide the details of each item with calories in below in a table format

               1. Item 1 - no of calories and grams
               2. Item 2 - no of calories and grams
               ----
               ----

Finally you can mention whether the food is healthy or not and also mention the percentage split of the ratio of protien,
carbohydrates(of which sugar also),fats,fibres,etc  in a concise manner.
    
"""

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(prompt,image_data,input)
    st.header("The Response is")
    st.write(response)

    
     