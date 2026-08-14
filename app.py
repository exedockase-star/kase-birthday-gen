import streamlit as st
from PIL import Image, ImageDraw
import os

st.set_page_config(page_title="KASE Birthday Generator")
st.title("KASE Birthday Wish Generator")

uploaded_file = st.file_uploader("Upload Employee Photo", type=["jpg", "png", "jpeg"])
name = st.text_input("Enter Name")
designation = st.text_input("Enter Designation")

if st.button("Generate Birthday Card"):
    if uploaded_file and name and designation:
        try:
            # 1. Load base template
            template_path = os.path.join(os.path.dirname(__file__), "template.png")
            template = Image.open(template_path).convert("RGBA")
            
            # 2. Create canvas
            canvas = Image.new("RGBA", template.size, (255, 255, 255, 255))
            
            # 3. Process employee photo to fit the exact inner frame dimensions
            photo = Image.open(uploaded_file).convert("RGBA")
            # Exact size to fit inside the inner card window
            photo = photo.resize((290, 335)) 
            
            # Paste photo at the exact inner window coordinates
            canvas.paste(photo, (82, 305)) 
            
            # 4. Paste the ID card template cleanly on top
            canvas.paste(template, (0, 0), template)
            
            # 5. Add Name and Designation text below the photo
            draw = ImageDraw.Draw(canvas)
            draw.text((95, 685), name, fill="black")
            draw.text((95, 725), designation, fill="black")
            
            # 6. Save final output
            final_image = canvas.convert("RGB")
            final_image.save("birthday_final.jpg", "JPEG")
            
            st.image("birthday_final.jpg")
            with open("birthday_final.jpg", "rb") as file:
                st.download_button("Download JPG", file, "birthday_final.jpg", "image/jpeg")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please upload a photo and fill in all fields.")
