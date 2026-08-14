import streamlit as st
from PIL import Image, ImageDraw
import os

# Page Title
st.set_page_config(page_title="KASE Birthday Generator")
st.title("KASE Birthday Wish Generator")

# 1. Inputs
uploaded_file = st.file_uploader("Upload Employee Photo", type=["jpg", "png", "jpeg"])
name = st.text_input("Enter Name (e.g., Smt. Yasoda N)")
designation = st.text_input("Enter Designation (e.g., Junior Executive)")

# 2. Processing
if st.button("Generate Birthday Card"):
    if uploaded_file and name and designation:
        try:
            # Load the base template
            template_path = os.path.join(os.path.dirname(__file__), "template.png")
            template = Image.open(template_path).convert("RGBA")
            
            # Load and process the uploaded photo
            photo = Image.open(uploaded_file).convert("RGBA")
            
            # --- ADJUSTED PHOTO SETTINGS ---
            # Resize photo to fit nicely inside the white ID window (Width, Height)
            photo = photo.resize((320, 380)) 
            
            # Paste photo lower down so it stays inside the card frame (X, Y)
            template.paste(photo, (95, 310)) 
            
            # Add Text
            draw = ImageDraw.Draw(template)
            
            # Drawing the text at the bottom of the white card
            # Adjust these Y coordinates if the text is too high or low
            draw.text((135, 780), name, fill="black")
            draw.text((135, 820), designation, fill="black")
            
            # Convert to RGB to save as JPEG
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
