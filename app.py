import streamlit as st
from PIL import Image, ImageDraw, ImageFont
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
            # Load assets
            template_path = os.path.join(os.path.dirname(__file__), "template.png")
            template = Image.open(template_path).convert("RGBA")
            photo = Image.open(uploaded_file).convert("RGBA")
            
            # --- PHOTO FIT SETTINGS ---
            # Resize photo to fill the light blue frame
            photo = photo.resize((315, 360)) 
            # Paste photo at (68, 285) - Adjust these if needed
            template.paste(photo, (68, 285)) 
            
            # --- TEXT SETTINGS ---
            draw = ImageDraw.Draw(template)
            
            # Define fonts (Uses default font; for custom fonts, upload a .ttf file to your repo)
            try:
                # If you upload a .ttf file to your repo, change 'arial.ttf' to your filename
                font_name = ImageFont.truetype("arial.ttf", 35)
                font_desig = ImageFont.truetype("arial.ttf", 25)
            except:
                font_name = ImageFont.load_default()
                font_desig = ImageFont.load_default()

            # Drawing the text (X=100, Y=720)
            draw.text((100, 720), name, fill="black", font=font_name)
            draw.text((100, 765), designation, fill="black", font=font_desig)
            
            # Save as JPEG
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
            st.error(f"Error: {e}")
    else:
        st.warning("Please upload a photo and fill in all fields.")
