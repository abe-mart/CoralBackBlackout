import streamlit as st
from PIL import Image, ImageOps, ImageFont, ImageDraw
import io
from zipfile import ZipFile
import tempfile
import os

from main import addShadow, createBlur, lightenImage

### Excluding Imports ###
st.title("Background Putter")

use_water = st.checkbox('Put Watermark')
uploaded_file = st.file_uploader("Choose outline image...", type="png",accept_multiple_files=False)
uploaded_file_2 = st.file_uploader("Choose blackout image...", type="png",accept_multiple_files=False)
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img2 = Image.open(uploaded_file_2)
    filename_up = uploaded_file.name.split('.')[0]
    # st.image(img, caption='Uploaded Image.', use_column_width=True)
    # st.image(img2, caption='Uploaded Image.', use_column_width=True)
    c = st.columns(2)
    with c[0]:
        x_scale_b = st.number_input('X Scale',1.0,format='%f')
        y_scale_b = st.number_input('Y Scale',1.0,format='%f')
    with c[1]:
        x_offset_b = st.number_input('X Offset')
        y_offset_b = st.number_input('Y Offset')
    st.write("")
    st.write("Putting Background...")
    
    # Prepare zip folder
    zip_buffer = io.BytesIO()
    zipList = []
    
    # Background 1 - Board
    foreground = ImageOps.contain(img,(2580,1186))
    blackout = ImageOps.contain(img2,(int(2580*x_scale_b),int(1186*y_scale_b)))
    background = Image.open('Images/Background1.jpg', 'r')
    watermark = Image.open('Images/Watermark_short.png','r')
    badge = Image.open('Images/badge.png','r')
    bg_w, bg_h = background.size
    
    background = addShadow(foreground,blackout,background,x_offset=0,y_offset=-50,x_blur_offset=0,y_blur_offset=3,lighten_amount=0,blur_amount=8,alpha_reduction=3.5,x_offset_b=x_offset_b,y_offset_b=y_offset_b)
    
    if use_water: background.paste(watermark, (0,331), watermark)
    
    font = ImageFont.truetype(font='Fonts/Bebas.ttf',size=248)
    draw = ImageDraw.Draw(im=background)
    draw.text(xy=(bg_w // 2, 166), text=filename_up, font=font, fill=(214,131,63), anchor='mm') 
    
    bg_w, bg_h = background.size
    background.paste(badge, (bg_w//2+800,bg_h//2-625), badge)
    
    img_byte_arr = io.BytesIO()
    background.save(img_byte_arr, format='jpeg')
    
    zipList.append([img_byte_arr,'background1.jpeg'])
    
    st.image(background, caption='Aligned image', use_column_width=True)
    
    # Background 1B - Two layers
    foreground = ImageOps.contain(img,(2580//2,1186//2))
    blackout = ImageOps.contain(img2,(2580//2,1186//2))
    background = Image.open('Images/Background1.jpg', 'r')
    watermark = Image.open('Images/Watermark_short.png','r')
    badge = Image.open('Images/badge.png','r')
    bg_w, bg_h = background.size
    
    x_offset=0
    y_offset=-50
    x_blur_offset=0
    y_blur_offset=3
    lighten_amount=0
    blur_amount=8
    alpha_reduction=3.5
    # background.paste(front, (0,0), front)
    
    blurred = createBlur(foreground,alpha_reduction,blur_amount)
    
    blackout_blurred = createBlur(blackout,alpha_reduction,blur_amount)

    foreground = lightenImage(foreground,lighten_amount)
    
    # blackout = lightenImage(blackout,100)
    color_overlay = Image.new('RGB', blackout.size, color=(131, 115, 100))
    # blackout = Image.alpha_composite(blackout, color_overlay)
    blackout.paste(color_overlay,(0,0),blackout)
    
    bg_w, bg_h = background.size
    img_w, img_h = foreground.size

    offset = ((bg_w - img_w) // 2 + x_offset - img_w//2, (bg_h - img_h) // 2 + y_offset)
    offset_blur = ((bg_w - img_w) // 2 + x_offset + x_blur_offset - img_w//2, (bg_h - img_h) // 2 + y_offset + y_blur_offset)
    blackout_offset = ((bg_w - img_w) // 2 + x_offset + img_w//2, (bg_h - img_h) // 2 + y_offset)
    blackout_offset_blur = ((bg_w - img_w) // 2 + x_offset + x_blur_offset + img_w//2, (bg_h - img_h) // 2 + y_offset + y_blur_offset)
    background.paste(blackout_blurred, blackout_offset_blur, blackout_blurred)
    background.paste(blackout, blackout_offset, blackout)
    background.paste(blurred, offset_blur, blurred)
    background.paste(foreground, offset, foreground)
    
    if use_water: background.paste(watermark, (0,0), watermark)
    
    # Title text
    font = ImageFont.truetype(font='Fonts/Bebas.ttf',size=248)
    draw = ImageDraw.Draw(im=background)
    draw.text(xy=(bg_w // 2, 166), text='Two  Layers', font=font, fill=(214,131,63), anchor='mm')
    
    img_byte_arr = io.BytesIO()
    background.save(img_byte_arr, format='jpeg')
    
    zipList.append([img_byte_arr,'background1b.jpeg'])
    
    # Background 2 - Boxes
    foreground = ImageOps.contain(img,(1800,1800))
    blackout = ImageOps.contain(img2,(1800,1800))
    background = Image.open('Images/Background2.jpg', 'r')
    watermark = Image.open('Images/Watermark.png','r')
    
    background = addShadow(foreground,blackout,background,x_offset=300,y_offset=0,x_blur_offset=3,y_blur_offset=-3)
    
    if use_water: background.paste(watermark, (0,0), watermark)
    
    img_byte_arr = io.BytesIO()
    background.save(img_byte_arr, format='jpeg')
    
    zipList.append([img_byte_arr,'background2.jpeg'])
    
    # Background 3 - Kitchen
    foreground = ImageOps.contain(img,(2195,915))
    blackout = ImageOps.contain(img2,(2195,915))
    background = Image.open('Images/Background3.jpg', 'r')
    watermark = Image.open('Images/Watermark.png','r')
    
    background = addShadow(foreground,blackout,background,x_offset=-180,y_offset=-500,x_blur_offset=3,y_blur_offset=-3,lighten_amount=50,blur_amount=8,alpha_reduction=3)
    
    if use_water: background.paste(watermark, (0,0), watermark)
    
    img_byte_arr = io.BytesIO()
    background.save(img_byte_arr, format='jpeg')
    
    zipList.append([img_byte_arr,'background3.jpeg'])
    
    # Background 4 - Cactus
    foreground = ImageOps.contain(img,(2597,1186))
    blackout = ImageOps.contain(img2,(2597,1186))
    background = Image.open('Images/Background4a.jpg', 'r')
    front = Image.open('Images/Background4b.png', 'r')
    watermark = Image.open('Images/Watermark.png','r')
    
    background = addShadow(foreground,blackout,background,x_offset=0,y_offset=-300,x_blur_offset=-3,y_blur_offset=1,lighten_amount=50,blur_amount=8,alpha_reduction=2.5)
    
    background.paste(front, (0,0), front)
    if use_water: background.paste(watermark, (0,0), watermark)
    
    img_byte_arr = io.BytesIO()
    background.save(img_byte_arr, format='jpeg')
    
    zipList.append([img_byte_arr,'background4.jpeg'])
    
    # Background 5 - Ladder
    foreground = ImageOps.contain(img,(2294,1005))
    blackout = ImageOps.contain(img2,(2294,1005))
    background = Image.open('Images/Background5a.jpg', 'r')
    front = Image.open('Images/Background5b.png', 'r')
    watermark = Image.open('Images/Watermark.png','r')
    
    background = addShadow(foreground,blackout,background,x_offset=-220,y_offset=-250,x_blur_offset=-1,y_blur_offset=0,lighten_amount=50,blur_amount=6,alpha_reduction=3.5)
    
    background.paste(front, (0,0), front)
    if use_water: background.paste(watermark, (0,0), watermark)
    
    img_byte_arr = io.BytesIO()
    background.save(img_byte_arr, format='jpeg')
    
    zipList.append([img_byte_arr,'background5.jpeg'])
    
    # Background 6 - Bag
    foreground = ImageOps.contain(img,(968,671))
    blackout = ImageOps.contain(img2,(968,671))
    background = Image.open('Images/Background6a.jpg', 'r')
    front = Image.open('Images/Background6b.png', 'r')
    watermark = Image.open('Images/Watermark.png','r')
    
    background = addShadow(foreground,blackout,background,x_offset=50,y_offset=200,x_blur_offset=0,y_blur_offset=0,lighten_amount=40,blur_amount=1.5,alpha_reduction=50)
    
    background.paste(front, (0,0), front)
    if use_water: background.paste(watermark, (0,0), watermark)
    
    img_byte_arr = io.BytesIO()
    background.save(img_byte_arr, format='jpeg')
    
    zipList.append([img_byte_arr,'background6.jpeg'])
    
    # Background 7 - Shirt
    foreground = ImageOps.contain(img,(1005,481))
    blackout = ImageOps.contain(img2,(1005,481))
    background = Image.open('Images/Background7a.jpg', 'r')
    front = Image.open('Images/Background7b.png', 'r')
    watermark = Image.open('Images/Watermark.png','r')
    
    background = addShadow(foreground,blackout,background,x_offset=25,y_offset=-200,x_blur_offset=0,y_blur_offset=0,lighten_amount=20,blur_amount=0,alpha_reduction=1)
    
    background.paste(front, (0,0), front)
    if use_water: background.paste(watermark, (0,0), watermark)
    
    img_byte_arr = io.BytesIO()
    background.save(img_byte_arr, format='jpeg')
    
    zipList.append([img_byte_arr,'background7.jpeg'])
    
    # Background 8 - Car
    foreground = ImageOps.contain(img,(1392,408))
    blackout = ImageOps.contain(img2,(1392,408))
    background = Image.open('Images/Background8.jpg', 'r')
    watermark = Image.open('Images/Watermark.png','r')
    
    background = addShadow(foreground,blackout,background,x_offset=-210,y_offset=-525,x_blur_offset=1,y_blur_offset=1,lighten_amount=10,blur_amount=1,alpha_reduction=1)
    
    if use_water: background.paste(watermark, (0,0), watermark)
    
    img_byte_arr = io.BytesIO()
    background.save(img_byte_arr, format='jpeg')
    
    zipList.append([img_byte_arr,'background8.jpeg'])
    
    # writing files to a zipfile
    with ZipFile(zip_buffer, 'w') as zip_file:
        with tempfile.TemporaryDirectory() as tmp:
            # writing each file one by one
            for file_and_name in zipList:
                with open(os.path.join(tmp,file_and_name[1]),"wb") as f:
                    f.write(file_and_name[0].getbuffer())
                zip_file.write(os.path.join(tmp,file_and_name[1]),file_and_name[1])
    
    st.download_button('Down It',data=zip_buffer,file_name=filename_up+'_listing_images.zip',mime="application/zip")