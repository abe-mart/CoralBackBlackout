import streamlit as st
from PIL import Image, ImageOps, ImageFont, ImageDraw
import io
from zipfile import ZipFile
import tempfile
import os

from main import addShadow

### Excluding Imports ###
st.title("Background Putter")

uploaded_file = st.file_uploader("Choose an image...", type="png",accept_multiple_files=False)
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    filename_up = uploaded_file.name.split('.')[0]
    st.image(img, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Putting Background...")
    
    # Prepare zip folder
    zip_buffer = io.BytesIO()
    zipList = []
    
    # Background 1 - Board
    foreground = ImageOps.contain(img,(2580,1186))
    background = Image.open('Images/Background1.jpg', 'r')
    bg_w, bg_h = background.size
    
    background = addShadow(foreground,background,x_offset=0,y_offset=-50,x_blur_offset=0,y_blur_offset=0,lighten_amount=0,blur_amount=0,alpha_reduction=3.5)
    
    font = ImageFont.truetype(font='Fonts/Bebas.ttf',size=248)
    draw = ImageDraw.Draw(im=background)
    draw.text(xy=(bg_w // 2, 166), text=filename_up, font=font, fill=(214,131,63), anchor='mm') 
    
    img_byte_arr = io.BytesIO()
    background.save(img_byte_arr, format='jpeg')
    
    zipList.append([img_byte_arr,'background1.jpeg'])
    
    # Background 2 - Boxes
    foreground = ImageOps.contain(img,(1800,1800))
    background = Image.open('Images/Background2.jpg', 'r')
    
    background = addShadow(foreground,background,x_offset=300,y_offset=0,x_blur_offset=3,y_blur_offset=-3)
    
    img_byte_arr = io.BytesIO()
    background.save(img_byte_arr, format='jpeg')
    
    zipList.append([img_byte_arr,'background2.jpeg'])
    
    # Background 3 - Kitchen
    foreground = ImageOps.contain(img,(2195,915))
    background = Image.open('Images/Background3.jpg', 'r')
    
    background = addShadow(foreground,background,x_offset=-180,y_offset=-500,x_blur_offset=3,y_blur_offset=-3,lighten_amount=50,blur_amount=8,alpha_reduction=3)
    
    img_byte_arr = io.BytesIO()
    background.save(img_byte_arr, format='jpeg')
    
    zipList.append([img_byte_arr,'background3.jpeg'])
    
    # Background 4 - Cactus
    foreground = ImageOps.contain(img,(2597,1186))
    background = Image.open('Images/Background4a.jpg', 'r')
    front = Image.open('Images/Background4b.png', 'r')
    
    background = addShadow(foreground,background,x_offset=0,y_offset=-300,x_blur_offset=-3,y_blur_offset=1,lighten_amount=50,blur_amount=8,alpha_reduction=2.5)
    
    background.paste(front, (0,0), front)
    
    img_byte_arr = io.BytesIO()
    background.save(img_byte_arr, format='jpeg')
    
    zipList.append([img_byte_arr,'background4.jpeg'])
    
    # Background 5 - Ladder
    foreground = ImageOps.contain(img,(2294,1005))
    background = Image.open('Images/Background5a.jpg', 'r')
    front = Image.open('Images/Background5b.png', 'r')
    
    background = addShadow(foreground,background,x_offset=-220,y_offset=-250,x_blur_offset=-1,y_blur_offset=0,lighten_amount=50,blur_amount=6,alpha_reduction=3.5)
    
    background.paste(front, (0,0), front)
    
    img_byte_arr = io.BytesIO()
    background.save(img_byte_arr, format='jpeg')
    
    zipList.append([img_byte_arr,'background5.jpeg'])
    
    # writing files to a zipfile
    with ZipFile(zip_buffer, 'w') as zip_file:
        with tempfile.TemporaryDirectory() as tmp:
            # writing each file one by one
            for file_and_name in zipList:
                with open(os.path.join(tmp,file_and_name[1]),"wb") as f:
                    f.write(file_and_name[0].getbuffer())
                zip_file.write(os.path.join(tmp,file_and_name[1]),file_and_name[1])
    
    st.download_button('Down It',data=zip_buffer,file_name=filename_up+'_listing_images.zip',mime="application/zip")