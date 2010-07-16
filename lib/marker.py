from PIL import Image,ImageDraw,ImageEnhance,ImageFont
from aggdraw import Draw, Pen, Brush


def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def make_marker(radius, fill_color, stroke_color, stroke_width, opacity=1.0,text=""):
    """
    Creates a map marker and returns a PIL image.

    radius
        In pixels

    fill_color
        Any PIL-acceptable color representation, but standard hex
        string is best

    stroke_color
        See fill_color

    stroke_width
        In pixels

    opacity
        Float between 0.0 and 1.0
        
    Text
        1 to 2 letter String 
    """
    # Double all dimensions for drawing. We'll resize back to the original
    # radius for final output -- it makes for a higher-quality image, especially
    # around the edges
    radius, stroke_width = radius * 2, stroke_width * 2
    diameter = radius * 2
    im = Image.new('RGBA', (diameter, diameter))
    draw = Draw(im)
    
    text=text
    
    # Move in from edges half the stroke width, so that the stroke is not
    # clipped.
    half_stroke_w = (stroke_width / 2 * 1.0) + 1
    min_x, min_y = half_stroke_w, half_stroke_w
    max_x = diameter - half_stroke_w
    max_y = max_x
    bbox = (min_x, min_y, max_x, max_y)
    margin=(radius/2,radius/2)
    # Translate opacity into aggdraw's reference (0-255)
    opacity = int(opacity * 255)
    draw.ellipse(bbox,
                 Pen(stroke_color, stroke_width, opacity),
                 Brush(fill_color, opacity))
    
    draw.flush()
    
    # The key here is to resize using the ANTIALIAS filter, which is very
    # high-quality
    #im = im.resize((diameter / 2, diameter / 2), Image.ANTIALIAS)
    textlayer = Image.new("RGBA", im.size, (0,0,0,0))
    textdraw = ImageDraw.Draw(textlayer)
    font = ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Arial.ttf', radius)
    
    textdraw.text((radius/4,radius/2), text,font=font)
#    if opacity != 1:
#        textlayer = reduce_opacity(textlayer,opacity)
    im=Image.composite(textlayer, im, textlayer)
    IM = im.resize((diameter / 2, diameter / 2), Image.ANTIALIAS)
    #im.save("/tmp/dummy.png", optimize=1)
    return IM



   
if __name__=="__main__":
    make_marker(10, "red", "white", 5, opacity=1.0)
    