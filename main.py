from PIL import Image, ImageOps, ImageFilter, ImageFont, ImageDraw



def lightenImage(image,amount=75):
    source = image.split()

    R, G, B, A = 0, 1, 2, 3
    constant = amount # constant by which each pixel is divided
    
    Red = source[R].point(lambda i: i + constant)
    Green = source[G].point(lambda i: i + constant)
    Blue = source[B].point(lambda i: i + constant)
    Alpha = source[A]
    
    image = Image.merge(image.mode, (Red, Green, Blue, Alpha))
    return image
    
def createBlur(image,alpha_reduction=2.5,blur_amount=7):
    source = image.split()

    R, G, B, A = 0, 1, 2, 3
    constant = 1.5 # constant by which each pixel is divided
    
    Red = source[R].point(lambda i: i/constant)
    Green = source[G].point(lambda i: i/constant)
    Blue = source[B].point(lambda i: i/constant)
    Alpha = source[A].point(lambda i: i/alpha_reduction)
    
    blurred = Image.merge(image.mode, (Red, Green, Blue, Alpha))
    
    blurred = blurred.filter(ImageFilter.BoxBlur(blur_amount))
    
    return blurred

def addShadow(foreground,blackout,background,x_offset=300,y_offset=0,x_blur_offset=3,y_blur_offset=-3,alpha_reduction=2.5,blur_amount=7,lighten_amount=75,x_offset_b=0,y_offset_b=0):

    blurred = createBlur(foreground,alpha_reduction,blur_amount)
    
    blackout_blurred = createBlur(blackout,alpha_reduction,blur_amount)

    foreground = lightenImage(foreground,lighten_amount)
    
    # blackout = lightenImage(blackout,100)
    color_overlay = Image.new('RGB', blackout.size, color=(131, 115, 100))
    # blackout = Image.alpha_composite(blackout, color_overlay)
    blackout.paste(color_overlay,(0,0),blackout)
    
    bg_w, bg_h = background.size
    img_w, img_h = foreground.size

    offset = ((bg_w - img_w) // 2 + x_offset, (bg_h - img_h) // 2 + y_offset)
    offset_blur = ((bg_w - img_w) // 2 + x_offset + x_blur_offset, (bg_h - img_h) // 2 + y_offset + y_blur_offset)
    blackout_offset = (int((bg_w - img_w) // 2 + x_offset + x_offset_b), int((bg_h - img_h) // 2 + y_offset + y_offset_b))
    blackout_offset_blur = (int((bg_w - img_w) // 2 + x_offset + x_blur_offset + x_offset_b), int((bg_h - img_h) // 2 + y_offset + y_blur_offset + y_offset_b))
    background.paste(blackout_blurred, blackout_offset_blur, blackout_blurred)
    background.paste(blackout, blackout_offset, blackout)
    background.paste(blurred, offset_blur, blurred)
    background.paste(foreground, offset, foreground)
    
    return background

def draw_text_psd_style(draw, xy, text, font, tracking=0, leading=None, **kwargs):
    """
    usage: draw_text_psd_style(draw, (0, 0), "Test", 
                tracking=-0.1, leading=32, fill="Blue")

    Leading is measured from the baseline of one line of text to the
    baseline of the line above it. Baseline is the invisible line on which most
    letters—that is, those without descenders—sit. The default auto-leading
    option sets the leading at 120% of the type size (for example, 12‑point
    leading for 10‑point type).

    Tracking is measured in 1/1000 em, a unit of measure that is relative to 
    the current type size. In a 6 point font, 1 em equals 6 points; 
    in a 10 point font, 1 em equals 10 points. Tracking
    is strictly proportional to the current type size.
    """
    def stutter_chunk(lst, size, overlap=0, default=None):
        for i in range(0, len(lst), size - overlap):
            r = list(lst[i:i + size])
            while len(r) < size:
                r.append(default)
            yield r
    x, y = xy
    font_size = font.size
    lines = text.splitlines()
    if leading is None:
        leading = font.size * 1.2
    for line in lines:
        for a, b in stutter_chunk(line, 2, 1, ' '):
            w = font.getlength(a + b) - font.getlength(b)
            # dprint("[debug] kwargs")
            print("[debug] kwargs:{}".format(kwargs))
                
            draw.text((x, y), a, font=font, **kwargs)
            x += w + (tracking / 1000) * font_size
        y += leading
        x = xy[0]


if __name__ == "__main__":
    
    foreground = Image.open('Images/mountaintest3.png', 'r')
    blackout = Image.open('Images/mountaintest3_blackout.png', 'r')
    foreground = ImageOps.contain(foreground,(2580,1186))
    blackout = ImageOps.contain(blackout,(2580,1186))
    img_w, img_h = foreground.size
    
    background = Image.open('Images/Background1.jpg', 'r')
    bg_w, bg_h = background.size
    
    front = Image.open('Images/Background7b.png', 'r')

    background = addShadow(foreground,blackout,background,x_offset=0,y_offset=-50,x_blur_offset=0,y_blur_offset=3,lighten_amount=0,blur_amount=8,alpha_reduction=3.5)
    
    # background.paste(front, (0,0), front)
    
    # Title text
    font = ImageFont.truetype(font='Fonts/Bebas.ttf',size=248)
    draw = ImageDraw.Draw(im=background)
    # draw.text(xy=(bg_w // 2, 166), text="Bearhat  Mountain", font=font, fill=(214,131,63), anchor='mm')   
    # text = "Bearhat  Mountain"
    # xy=(bg_w // 2, 166)
    # draw_text_psd_style(draw, xy, text, font, tracking=0, leading=None, **kwargs)
    
    badge = Image.open('Images/badge.png','r')
    bg_w, bg_h = background.size
    background.paste(badge, (bg_w//2+800,bg_h//2-625), badge)
    
    background.show()
    
    # background.save('Images\out.jpg')
    
    ## Two layers
    
    foreground = Image.open('Images/mountaintest3.png', 'r')
    blackout = Image.open('Images/mountaintest3_blackout.png', 'r')
    foreground = ImageOps.contain(foreground,(2580//2,1186//2))
    blackout = ImageOps.contain(blackout,(2580//2,1186//2))
    img_w, img_h = foreground.size
    
    background = Image.open('Images/Background1.jpg', 'r')
    bg_w, bg_h = background.size
    
    # front = Image.open('Images/Background7b.png', 'r')

    # background = addShadow(foreground,blackout,background,x_offset=0,y_offset=-50,x_blur_offset=0,y_blur_offset=3,lighten_amount=0,blur_amount=8,alpha_reduction=3.5)
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
    
    # Title text
    font = ImageFont.truetype(font='Fonts/Bebas.ttf',size=248)
    draw = ImageDraw.Draw(im=background)
    draw.text(xy=(bg_w // 2, 166), text='Two  Layers', font=font, fill=(214,131,63), anchor='mm') 
    
    # badge = Image.open('Images/badge.png','r')
    # bg_w, bg_h = background.size
    # background.paste(badge, (bg_w//2+800,bg_h//2-625), badge)
    
    background.show()