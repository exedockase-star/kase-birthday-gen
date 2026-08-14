import streamlit as st
from PIL import Image, ImageDraw, ImageOps
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

            # 1. Resize photo to fit the frame area
            photo = photo.resize((290, 335))

            # 2. Create a copy of the template to use as a mask
            # This creates a 'hole' where the photo should go
            mask = Image.new("L", template.size, 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.rectangle([82, 305, 372, 640], fill=255)

            # 3. Create the final image
            # We paste the photo first
            final_img = Image.new("RGBA", template.size, (255, 255, 255, 255))
            final_img.paste(photo, (82, 305))
            
            # 4. Now paste the template ON TOP using the mask to keep the photo inside the hole
            final_img.paste(template, (0, 0), template)

            # 5. Add Text
            draw = ImageDraw.Draw(final_img)
            draw.text((95, 685), name, fill="black")
            draw.text((95, 725), designation, fill="black")

            # Save and show
            final_rgb = final_img.convert("RGB")
            final_rgb.save("birthday_final.jpg", "JPEG")
            st.image("birthday_final.jpg")
            
            with open("birthday_final.jpg", "rb") as file:
                st.download_button("Download", file, "birthday_final.jpg", "image/jpeg")

        except Exception as e:
            st.error(f"Error: {e}")
