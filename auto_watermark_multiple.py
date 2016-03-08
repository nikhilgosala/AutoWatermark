import os
from PIL import Image, ExifTags

def preprocessImages(image_path, wm_path):
    "Open the images and resize the watermark to the required size"
    is_landscape = False
    is_potrait = False
    wm = {}
    
    #Open the images 
    try:
        image = Image.open(image_path)
    except:
        print("Please check the path of the image to be watermarked")
        quit()

    for i in range(len(wm_path)):  
        try:
            wm[i] = Image.open(wm_path[i])
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
            if(orientation in exif):
                orientation = exif[orientation] 

            if orientation == 3:   image = image.transpose(Image.ROTATE_180)
            elif orientation == 6: image = image.transpose(Image.ROTATE_270)
            elif orientation == 8: image = image.transpose(Image.ROTATE_90)

    wm_width = {}
    wm_height = {}
    #Get the dimensions of the images
    image_width, image_height = image.size
    for i in range(len(wm)):
        wm_width[i], wm_height[i] = wm[i].size

    #Check if the image is a landscape or a potrait image
    if image_width >= image_height:
        is_landscape = True
    else:
        is_potrait = True

    wm_height_new = {}
    wm_width_new = {}
    #Get the dimensions of the watermark to 10% of the width(In case of potrait) and 10% of the height(In case of landscape)
    for i in range(len(wm)):
        if(is_landscape):
            wm_height_new[i] = 0.08*image_height
            wm_width_new[i] = (wm_height_new[i]/wm_height[i])*wm_width[i]
            wm_height[i], wm_width[i] = wm_height_new[i], wm_width_new[i]
        elif(is_potrait):
            wm_height_new[i] = 0.1*image_width
            wm_width_new[i] = (wm_height_new[i]/wm_height[i])*wm_width[i]
            wm_height[i], wm_width[i] = wm_height_new[i], wm_width_new[i]
        
        #Resize the watermark
        wm[i].thumbnail((wm_width[i], wm_height[i]), Image.ANTIALIAS)
    
    return image, wm

def overlay(image, wm, pos):
    "Overlay the watermark over the image"
    wm_width = {}
    wm_height = {}
    overlay = image
    image_width, image_height = image.size
    for i in range(len(wm)):
        wm_width[i], wm_height[i] = wm[i].size

        if pos[i] == 'TL':
            overlay.paste(wm[i], (40, 40), wm[i])
        elif pos[i] == 'TR':
            overlay.paste(wm[i], (image_width-wm_width[i]-40, 40), wm[i])
        elif pos[i] == 'BL':
            overlay.paste(wm[i], (40, image_height-wm_height[i]-40), wm[i])
        elif pos[i] == 'BR':
            overlay.paste(wm[i],(image_width-wm_width[i]-40, image_height-wm_height[i]-40), wm[i])

    #overlay.show()

    return overlay
    #overlay.save(imagename + "_edit.jpg", "JPEG")
    

if __name__ == '__main__':
    num = int(input("Enter the number of watermarks\n"))
    watermark_path = {}
    watermark_pos = {}
    for i in range(num):
        path = input("Enter the path of the watermark\n")
        pos = input("Enter location of watermark(TL, TR, BL, BR)\n").upper()
        watermark_path[i] = path
        watermark_pos[i] = pos
    path = os.getcwd()
    images = os.listdir()
    if not os.path.isdir("Watermarked"):
        os.mkdir("Watermarked")
    
    for imagename in images:
        #if(imagename.endswith('.jpg') or imagename.endswith('.JPG') and not imagename.startswith('w_')):
        if not imagename.startswith('w_') and not imagename.endswith('.py'):
            print(imagename)
            image_path = imagename
            image, wm = preprocessImages(os.path.join(path,image_path), watermark_path)
            overlay_image = overlay(image,wm,watermark_pos)
            save_path = path + '\\Watermarked'
            overlay_image.save(os.path.join(save_path,imagename.split('.')[0]) + '_wm.jpg', 'JPEG')
    #image_path = input("Enter the path of the image to be watermarked\n")
    #watermark_path = input("Enter the path of the watermark\n")
    #pos = input("Enter location of watermark(TL, TR, BL, BR)\n").upper()
    
    
    
