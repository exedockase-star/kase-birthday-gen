import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

st.set_page_config(page_title="KASE Birthday Generator", layout="wide")
st.title("KASE Birthday Wish Generator")

# Sidebar for precise adjustments
st.sidebar.header("🛠️ Adjustment Panel")
px = st.sidebar.slider("Photo X", 0, 500, 95)
py = st.sidebar.slider("Photo Y", 0, 500, 305)
pw = st.sidebar.slider("Photo Width", 100, 500, 305)
ph = st.sidebar.slider("Photo Height", 100, 500, 335)
corner_radius = st.sidebar.slider("Corner Radius", 0, 50, 20)

uploaded_file = st.file_uploader("Upload Employee Photo", type=["jpg", "png", "jpeg"])
name = st.text_input("Enter Name", "Employee Name")
desig = st.text_input("Enter Designation", "Designation")

if st.button("Generate Birthday Card"):
    if uploaded_file and name and desig:
        try:
            # Load Template
            canvas = Image.open("template.png").convert("RGBA")
            
            # Process Photo with Rounded Corners
            photo = Image.open(uploaded_file).convert("RGBA").resize((pw, ph))
            mask = Image.new("L", (pw, ph), 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.rounded_rectangle((0, 0, pw, ph), radius=corner_radius, fill=255)
            
            # Apply rounded mask
            rounded_photo = ImageOps.fit(photo, (pw, ph), centering=(0.5, 0.5))
            rounded_photo.putalpha(mask)
            
            # Paste Photo
            canvas.paste(rounded_photo, (px, py), rounded_photo)
            
            # --- FONT LOADING WITH FAILSAFE ---
            draw = ImageDraw.Draw(canvas)
            try:
                # This points to the file in the same folder as app.py
                font_bold = ImageFont.truetype(os.path.join(os.path.dirname(__file__), "NotoSerifCondensed-Bold.ttf"), 32)
                font_reg = ImageFont.truetype(os.path.join(os.path.dirname(__file__), "NotoSerifCondensed-Regular.ttf"), 22)
            except:
                st.warning("Custom fonts not found. Using default font.")
                font_bold = ImageFont.load_default()
                font_reg = ImageFont.load_default()
            
            draw.text((100, 660), name, fill="black", font=font_bold)
            draw.text((100, 705), desig, fill="black", font=font_reg)
            
            # Save
            final = canvas.convert("RGB")
            final.save("birthday_final.jpg", "JPEG")
            st.image("birthday_final.jpg")
            with open("birthday_final.jpg", "rb") as f:
                st.download_button("Download JPG", f, "birthday_final.jpg", "image/jpeg")
        except Exception as e:
            st.error(f"Error: {e}")
