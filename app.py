import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

st.set_page_config(page_title="KASE Birthday Generator", layout="wide")
st.title("KASE Birthday Wish Generator")

# Sidebar Adjusters
st.sidebar.header("🛠️ Adjustment Panel")
px = st.sidebar.slider("Photo Left / Right (X)", 0, 800, 94)
py = st.sidebar.slider("Photo Up / Down (Y)", 0, 1000, 380)
pw = st.sidebar.slider("Photo Width", 50, 800, 418)
ph = st.sidebar.slider("Photo Height", 50, 1000, 442)
corner_radius = st.sidebar.slider("Corner Radius", 0, 50, 20)
text_y = st.sidebar.slider("Text Up / Down (Y)", 0, 1200, 829)

uploaded_file = st.file_uploader("Upload Employee Photo", type=["jpg", "png", "jpeg"])
name = st.text_input("Enter Name", "Employee Name")
desig = st.text_input("Enter Designation", "Designation")

# --- LIVE PREVIEW LOGIC ---
if uploaded_file and name and desig:
    try:
        # Load Template
        canvas = Image.open("template.png").convert("RGBA")
        
        # Process Photo
        photo = Image.open(uploaded_file).convert("RGBA").resize((pw, ph))
        mask = Image.new("L", (pw, ph), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle((0, 0, pw, ph), radius=corner_radius, fill=255)
        
        rounded_photo = ImageOps.fit(photo, (pw, ph), centering=(0.5, 0.5))
        rounded_photo.putalpha(mask)
        canvas.paste(rounded_photo, (px, py), rounded_photo)
        
        # Draw Text (Noto Serif Ethiopic)
        draw = ImageDraw.Draw(canvas)
        try:
            # Pointing to the new Ethiopic font files
            font_bold = ImageFont.truetype(os.path.join(os.path.dirname(__file__), "NotoSerifEthiopic-Bold.ttf"), 45)
            font_reg = ImageFont.truetype(os.path.join(os.path.dirname(__file__), "NotoSerifEthiopic-Regular.ttf"), 32)
        except:
            font_bold = ImageFont.load_default()
            font_reg = ImageFont.load_default()
            st.warning("⚠️ Custom fonts not found. Please upload 'NotoSerifEthiopic-Bold.ttf' and 'NotoSerifEthiopic-Regular.ttf' to GitHub.")
        
        # Spacing reduced to 35
        draw.text((100, text_y), name, fill="black", font=font_bold)
        draw.text((100, text_y + 40), desig, fill="black", font=font_reg)
        
        # Save and show live preview
        final = canvas.convert("RGB")
        final.save("birthday_final.jpg", "JPEG")
        st.image("birthday_final.jpg", use_container_width=True)
        
        with open("birthday_final.jpg", "rb") as f:
            st.download_button("📥 Download Final JPG", f, "birthday_final.jpg", "image/jpeg")
            
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Upload a photo and enter details to see the live preview.")
