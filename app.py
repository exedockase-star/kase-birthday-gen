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
            # 1. Load the template base
            template_path = os.path.join(os.path.dirname(__file__), "template.png")
            canvas = Image.open(template_path).convert("RGBA")
            
            # 2. Resize photo to completely fill the inner frame box
            photo = Image.open(uploaded_file).convert("RGBA")
            photo = photo.resize((305, 335))  # Adjusted width & height to cover the inner border
            
            # 3. Paste photo shifted right to align with the frame
            canvas.paste(photo, (95, 305))  # X=95 moves it right, Y=305 aligns the top
            
            # 4. Draw Name and Designation cleanly in the lower white space
            draw = ImageDraw.Draw(canvas)
            
            try:
                font_name = ImageFont.truetype("arial.ttf", 26)
                font_desig = ImageFont.truetype("arial.ttf", 18)
            except:
                font_name = ImageFont.load_default()
                font_desig = ImageFont.load_default()

            draw.text((100, 660), name, fill="black", font=font_name)
            draw.text((100, 700), designation, fill="black", font=font_desig)
            
            # 5. Save and output final JPG
            final_image = canvas.convert("RGB")
            final_image.save("birthday_final.jpg", "JPEG")
            
            st.image("birthday_final.jpg")
            with open("birthday_final.jpg", "rb") as file:
                st.download_button("Download JPG", file, "birthday_final.jpg", "image/jpeg")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please upload a photo and fill in all fields.")
