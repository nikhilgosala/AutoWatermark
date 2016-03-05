__author__ = 'Nikhil Bharadwaj'
__license__ = 'MIT License'
__version__ = 'Python 3.5'

import os
from PIL import Image, ExifTags

def preprocessImages(image_path, wm_path):
    "Open the images and resize the watermark to the required size"
    is_landscape = False
    is_potrait = False
    
    #Open the images 
    try:
        image = Image.open(image_path)
    except:
        print("Please check the path of the image to be watermarked")
        quit()
        
    try:
        wm = Image.open(wm_path)
    except:
        print("Please check the path of the watermark")
        quit()
		
	 #Rotate the image if it was in potrait mode. Use the EXIF tags stored by the camera in the JPEG file
    if hasattr(image, '_getexif'): # only present in JPEGs
        for orientation in ExifTags.TAGS.keys(): 
            if ExifTags.TAGS[orientation]=='Orientation':   #Find where the Orientation header is
                break 
        e = image._getexif()       # returns None if no EXIF data
        if e is not None:
            exif=dict(e.items())
            orientation = exif[orientation] 

            if orientation == 3:   image = image.transpose(Image.ROTATE_180)
            elif orientation == 6: image = image.transpose(Image.ROTATE_270)
            elif orientation == 8: image = image.transpose(Image.ROTATE_90)

    #Get the dimensions of the images
    image_width, image_height = image.size
    wm_width, wm_height = wm.size

    #Check if the image is a landscape or a potrait image
    if image_width >= image_height:
        is_landscape = True
    else:
        is_potrait = True

    #Get the dimensions of the watermark to 10% of the width(In case of potrait) and 10% of the height(In case of landscape)
    if(is_landscape):
        wm_height_new = 0.08*image_height
        wm_width_new = (wm_height_new/wm_height)*wm_width
        wm_height, wm_width = wm_height_new, wm_width_new
    elif(is_potrait):
        wm_height_new = 0.08*image_width
        wm_width_new = (wm_height_new/wm_height)*wm_width
        wm_height, wm_width = wm_height_new, wm_width_new
        
    #Resize the watermark
    wm.thumbnail((wm_width, wm_height), Image.ANTIALIAS)
    
    return image, wm

def overlay(image, wm, pos):
    "Overlay the watermark over the image"
    overlay = image
    image_width, image_height = image.size
    wm_width, wm_height = wm.size

    if pos == 'TL':
        overlay.paste(wm, (40, 40), wm)
    elif pos == 'TR':
        overlay.paste(wm, (image_width-wm_width-40, 40), wm)
    elif pos == 'BL':
        overlay.paste(wm, (40, image_height-wm_height-40), wm)
    elif pos == 'BR':
        overlay.paste(wm,(image_width-wm_width-40, image_height-wm_height-40), wm)

    #overlay.show()

    return overlay
    #overlay.save(imagename + "_edit.jpg", "JPEG")
    

if __name__ == '__main__':

    watermark_path = input("Enter the path of the watermark\n")
    pos = input("Enter location of watermark(TL, TR, BL, BR)\n").upper()
    path = os.getcwd()
    images = os.listdir()
    if not os.path.isdir("Watermarked"):
        os.mkdir("Watermarked")
    
    for imagename in images:
        if(imagename.endswith('.jpg') or imagename.endswith('.JPG') and not imagename.startswith('wm')):
            print(imagename)
            image_path = imagename
            image, wm = preprocessImages(os.path.join(path,image_path), watermark_path)
            overlay_image = overlay(image,wm,pos)
            save_path = path + '\\Watermarked'
            overlay_image.save(os.path.join(save_path,imagename) + '_wm.jpg', 'JPEG')
    #image_path = input("Enter the path of the image to be watermarked\n")
    #watermark_path = input("Enter the path of the watermark\n")
    #pos = input("Enter location of watermark(TL, TR, BL, BR)\n").upper()
    
    
    
