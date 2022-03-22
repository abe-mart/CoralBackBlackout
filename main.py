from PIL import Image, ImageOps, ImageFilter



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

def addShadow(foreground,background,x_offset=300,y_offset=0,x_blur_offset=3,y_blur_offset=-3,alpha_reduction=2.5,blur_amount=7,lighten_amount=75):

    blurred = createBlur(foreground,alpha_reduction,blur_amount)

    foreground = lightenImage(foreground,lighten_amount)
    
    bg_w, bg_h = background.size
    img_w, img_h = foreground.size

    offset = ((bg_w - img_w) // 2 + x_offset, (bg_h - img_h) // 2 + y_offset)
    offset_blur = ((bg_w - img_w) // 2 + x_offset + x_blur_offset, (bg_h - img_h) // 2 + y_offset + y_blur_offset)
    background.paste(blurred, offset_blur, blurred)
    background.paste(foreground, offset, foreground)
    
    return background


if __name__ == "__main__":
    
    foreground = Image.open('Images\mountaintest.png', 'r')
    foreground = ImageOps.contain(foreground,(2597,1186))
    img_w, img_h = foreground.size
    
    background = Image.open('Images\Background4a.jpg', 'r')
    bg_w, bg_h = background.size
    
    front = Image.open('Images\Background4b.png', 'r')

    background = addShadow(foreground,background,x_offset=0,y_offset=-300,x_blur_offset=-3,y_blur_offset=1,lighten_amount=50,blur_amount=8,alpha_reduction=2.5)
    
    background.paste(front, (0,0), front)
    
    background.show()
    
    # background.save('Images\out.jpg')