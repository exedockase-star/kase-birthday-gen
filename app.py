import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# Page Title
st.set_page_config(page_title="KASE Birthday Generator")
st.title("KASE Birthday Wish Generator")

# 1. Inputs
uploaded_file = st.file_uploader("Upload Employee Photo", type=["jpg", "png"])
name = st.text_input("Enter Name")
designation = st.text_input("Enter Designation")

# 2. Processing
if st.button("Generate Birthday Card"):
    if uploaded_file and name and designation:
        # Load the base template
        template = Image.open("template.png").convert("RGBA")
        photo = Image.open(uploaded_file).convert("RGBA")
        
        # --- ADJUST COORDINATES HERE ---
        # Resize photo (Width, Height)
        photo = photo.resize((400, 400)) 
        
        # Paste photo (X, Y) - adjust these numbers based on your template
        template.paste(photo, (150, 200)) 
        
        # Add Text
        draw = ImageDraw.Draw(template)
        
        # Drawing the text (X, Y) - adjust these based on your template
        draw.text((150, 650), name, fill="black")
        draw.text((150, 700), designation, fill="black")
        
        # Save to a temporary file
        template.save("birthday_final.jpg")
        
        # Display and Download
        st.image("birthday_final.jpg")
        with open("birthday_final.jpg", "rb") as file:
            st.download_button("Download JPG", file, "birthday_final.jpg", "image/jpeg")
    else:
        st.warning("Please upload a photo and fill in both name and designation.")