import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os

st.set_page_config(page_title="KASE Birthday Generator", layout="wide")
st.title("KASE Birthday Wish Generator")

# --- LIVE ADJUSTMENT SLIDERS IN THE SIDEBAR ---
st.sidebar.header("🛠️ Position Adjuster")
st.sidebar.info("Drag these sliders to instantly move the photo and text into place on your live preview!")

photo_x = st.sidebar.slider("Photo Left / Right (X)", 0, 500, 95)
photo_y = st.sidebar.slider("Photo Up / Down (Y)", 0, 500, 305)
photo_w = st.sidebar.slider("Photo Width", 100, 500, 305)
photo_h = st.sidebar.slider("Photo Height", 100, 500, 335)
text_y = st.sidebar.slider("Text Up / Down (Y)", 500, 900, 660)

# --- MAIN INPUTS ---
uploaded_file = st.file_uploader("Upload Employee Photo", type=["jpg", "png", "jpeg"])
name = st.text_input("Enter Name", "Smt. Kavya J Mohan")
designation = st.text_input("Enter Designation", "Executive - Skill Convergence")

if uploaded_file and name and designation:
    try:
        # Load template
        template_path = os.path.join(os.path.dirname(__file__), "template.png")
        canvas = Image.open(template_path).convert("RGBA")
        
        # Resize and paste photo using the live slider values
        photo = Image.open(uploaded_file).convert("RGBA")
        photo = photo.resize((photo_w, photo_h))
        canvas.paste(photo, (photo_x, photo_y))
        
        # Draw text using the live slider value
        draw = ImageDraw.Draw(canvas)
        try:
            font_name = ImageFont.truetype("arial.ttf", 26)
            font_desig = ImageFont.truetype("arial.ttf", 18)
        except:
            font_name = ImageFont.load_default()
            font_desig = ImageFont.load_default()

        draw.text((100, text_y), name, fill="black", font=font_name)
        draw.text((100, text_y + 40), designation, fill="black", font=font_desig)
        
        # Save and display live preview
        final_image = canvas.convert("RGB")
        final_image.save("birthday_final.jpg", "JPEG")
        
        st.image("birthday_final.jpg", caption="Live Preview (Adjust sliders on the left if anything is out of place)")
        
        # Download button
        with open("birthday_final.jpg", "rb") as file:
            st.download_button(
                label="📥 Download Final JPG", 
                data=file, 
                file_name="birthday_final.jpg", 
                mime="image/jpeg"
            )
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please upload an employee photo and enter their name/designation to see the live preview.")
