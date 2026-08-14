import streamlit as st
from PIL import Image, ImageDraw
import os

# Page Title
st.set_page_config(page_title="KASE Birthday Generator")
st.title("KASE Birthday Wish Generator")

# 1. Inputs
uploaded_file = st.file_uploader("Upload Employee Photo", type=["jpg", "png", "jpeg"])
name = st.text_input("Enter Name")
designation = st.text_input("Enter Designation")

# 2. Processing
if st.button("Generate Birthday Card"):
    if uploaded_file and name and designation:
        try:
            # Load the base template
            template_path = os.path.join(os.path.dirname(__file__), "template.png")
            template = Image.open(template_path).convert("RGBA")
            
            # Load and process the uploaded photo
            photo = Image.open(uploaded_file).convert("RGBA")
            
            # --- ADJUST COORDINATES HERE ---
            # Resize photo (Width, Height)
            photo = photo.resize((350, 350)) 
            
            # Paste photo (X, Y) - adjust these numbers based on your template
            # Coordinates: (left, top)
            template.paste(photo, (150, 250)) 
            
            # Add Text
            draw = ImageDraw.Draw(template)
            
            # Drawing the text (X, Y) - adjust these based on your template
            # You can also change the font size if needed
            draw.text((150, 650), name, fill="black")
            draw.text((150, 700), designation, fill="black")
            
            # --- FIX: Convert to RGB before saving as JPEG ---
            # JPEG doesn't support transparency, so we must convert to RGB
            final_image = template.convert("RGB")
            final_image.save("birthday_final.jpg", "JPEG")
            
            # Display and Download
            st.image("birthday_final.jpg")
            with open("birthday_final.jpg", "rb") as file:
                st.download_button(
                    label="Download JPG", 
                    data=file, 
                    file_name="birthday_final.jpg", 
                    mime="image/jpeg"
                )
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload a photo and fill in both name and designation.")
