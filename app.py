import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

st.set_page_config(page_title="KASE Birthday Generator")
st.title("KASE Birthday Wish Generator")

uploaded_file = st.file_uploader("Upload Employee Photo", type=["jpg", "png", "jpeg"])
name = st.text_input("Enter Name")
designation = st.text_input("Enter Designation")

if st.button("Generate Birthday Card"):
    if uploaded_file and name and designation:
        try:
            # Load template
            template_path = os.path.join(os.path.dirname(__file__), "template.png")
            canvas = Image.open(template_path).convert("RGBA")
            
            # Open and resize photo to match the exact tall inner window frame slot
            photo = Image.open(uploaded_file).convert("RGBA")
            photo = photo.resize((290, 335))  # Exact width and height to cover the inner frame
            
            # Paste photo precisely into the inner window coordinates
            canvas.paste(photo, (82, 305))  # Exact X, Y matching the card's inner frame
            
            # Draw Name and Designation text below the photo window
            draw = ImageDraw.Draw(canvas)
            
            try:
                font_name = ImageFont.truetype("arial.ttf", 26)
                font_desig = ImageFont.truetype("arial.ttf", 18)
            except:
                font_name = ImageFont.load_default()
                font_desig = ImageFont.load_default()

            draw.text((90, 655), name, fill="black", font=font_name)
            draw.text((90, 695), designation, fill="black", font=font_desig)
            
            # Save and output final JPG
            final_image = canvas.convert("RGB")
            final_image.save("birthday_final.jpg", "JPEG")
            
            st.image("birthday_final.jpg")
            with open("birthday_final.jpg", "rb") as file:
                st.download_button("Download JPG", file, "birthday_final.jpg", "image/jpeg")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please upload a photo and fill in all fields.")
