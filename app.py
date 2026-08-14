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
            # Load assets
            template_path = os.path.join(os.path.dirname(__file__), "template.png")
            template = Image.open(template_path).convert("RGBA")
            photo = Image.open(uploaded_file).convert("RGBA")
            
            # Create a blank canvas
            canvas = Image.new("RGBA", template.size, (255, 255, 255, 255))
            
            # 1. Resize photo (adjust these if the photo looks too big/small)
            photo = photo.resize((315, 360)) 
            
            # 2. Paste photo first (Underneath)
            canvas.paste(photo, (68, 285)) 
            
            # 3. Paste template on top (The template's transparent "hole" will show the photo)
            canvas.paste(template, (0, 0), template)
            
            # 4. Add Text
            draw = ImageDraw.Draw(canvas)
            draw.text((100, 720), name, fill="black")
            draw.text((100, 765), designation, fill="black")
            
            # Save
            final_image = canvas.convert("RGB")
            final_image.save("birthday_final.jpg", "JPEG")
            
            st.image("birthday_final.jpg")
            with open("birthday_final.jpg", "rb") as file:
                st.download_button("Download JPG", file, "birthday_final.jpg", "image/jpeg")
        except Exception as e:
            st.error(f"Error: {e}")
