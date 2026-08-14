import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import A4

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

if uploaded_file and name and desig:
    try:
        # Load Template
        canvas_img = Image.open("template.png").convert("RGBA")
        
        # Process Photo
        photo = Image.open(uploaded_file).convert("RGBA").resize((pw, ph))
        mask = Image.new("L", (pw, ph), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle((0, 0, pw, ph), radius=corner_radius, fill=255)
        
        rounded_photo = ImageOps.fit(photo, (pw, ph), centering=(0.5, 0.5))
        rounded_photo.putalpha(mask)
        canvas_img.paste(rounded_photo, (px, py), rounded_photo)
        
        # Draw Text
        draw = ImageDraw.Draw(canvas_img)
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        try:
            font_bold = ImageFont.truetype(os.path.join(base_path, "NotoSerifEthiopic-Bold.ttf"), 40)
            font_reg = ImageFont.truetype(os.path.join(base_path, "NotoSerifEthiopic-Regular.ttf"), 32)
        except:
            font_bold = ImageFont.load_default()
            font_reg = ImageFont.load_default()
        
        draw.text((100, text_y), name, fill="black", font=font_bold)
        draw.text((100, text_y + 55), desig, fill="black", font=font_reg)
        
        # Save Preview
        final = canvas_img.convert("RGB")
        final.save("birthday_final.jpg", "JPEG")
        st.image("birthday_final.jpg", use_container_width=True)
        
        # Download Options
        col1, col2 = st.columns(2)
        with open("birthday_final.jpg", "rb") as f:
            col1.download_button("📥 Download JPG", f, "birthday_final.jpg", "image/jpeg")
            
        # PDF Generation
        pdf_path = "birthday_final.pdf"
        c = pdf_canvas.Canvas(pdf_path, pagesize=A4)
        c.drawImage("birthday_final.jpg", 0, 0, width=595, height=842) # A4 size
        c.save()
        
        with open(pdf_path, "rb") as f:
            col2.download_button("📄 Download PDF", f, "birthday_final.pdf", "application/pdf")
            
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Upload a photo and enter details to see the live preview.")
