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
            # Load the template
            template_path = os.path.join(os.path.dirname(__file__), "template.png")
            template = Image.open(template_path).convert("RGBA")
            
            # --- AUTOMATICALLY PUNCH A HOLE IN THE TEMPLATE ---
            # This clears the inner window area so you don't need a transparent PNG from Canva
            draw_temp = ImageDraw.Draw(template)
            # Coordinates for the inner frame window: [left, top, right, bottom]
            draw_temp.rectangle([68, 285, 383, 645], fill=(0, 0, 0, 0))
            
            # Create a clean white background canvas
            canvas = Image.new("RGBA", template.size, (255, 255, 255, 255))
            
            # Load and resize the employee photo
            photo = Image.open(uploaded_file).convert("RGBA")
            photo = photo.resize((315, 360)) 
            
            # Step 1: Paste the photo first (it sits safely in the background)
            canvas.paste(photo, (68, 285)) 
            
            # Step 2: Paste the template on top (the punched-out hole reveals the photo like a frame)
            canvas.paste(template, (0, 0), template)
            
            # Step 3: Add Name and Designation text below the photo
            draw = ImageDraw.Draw(canvas)
            draw.text((100, 720), name, fill="black")
            draw.text((100, 765), designation, fill="black")
            
            # Save and output final JPG
            final_image = canvas.convert("RGB")
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
