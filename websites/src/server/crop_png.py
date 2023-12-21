from PIL import Image, ImageDraw

def crop_png(png, x, y, w, h): 

    #image_path = png_path + name + '.png'
    #mark_save_path = mark_path + name + '.png'
    img = png
    crop_box = (x, y, x+w, y+h)
    draw = ImageDraw.Draw(img)
    draw.rectangle(crop_box, outline="red")
    
    #img.save(mark_save_path)
    return img