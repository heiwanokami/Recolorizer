from PIL import Image
import numpy as np
import os

#get files to recolor
    # get file.py path
current_dir = os.getcwd()

#get source files
source_dir = os.path.join(current_dir, "source images")
source_files = os.listdir(source_dir)

#set source and destination color
source_color = (40,40,40) #RGB format
dest_color = (231, 122, 128) #RGB format

#set destination folder - create if not exists
dest_folder = str(dest_color)

dest_dir = os.path.join(current_dir, dest_folder)
if os.path.exists(dest_dir):
    pass
else:
    os.mkdir(dest_dir)

dest_files = os.listdir(dest_dir)


#get recolorized files
dest_files = os.listdir(dest_dir)

#get diference between source and desti to avoid double processing
diff_files = []

for img in source_files:
    if img in dest_files:
        pass
    else:
        diff_files.append(img)


print(len(diff_files))


#recolorize the imgs and save them to defualt folder
if len(diff_files) == 0:
    print("no new files to recolorize...")
else:
    counter = 0
    for image in diff_files:

        img = Image.open(os.path.join(source_dir, image))

        # print(img.mode) #RGB
        # print(img.size)

        width = img.size[0] 
        height = img.size[1] 
        for i in range(0,width):# process all pixels
            for j in range(0,height):
                data = img.getpixel((i,j))
                #print(data) #(255, 255, 255)
                if (data[0]==40 and data[1]==40 and data[2]==40):
                    img.putpixel((i,j),(231, 122, 128))
        img.save(os.path.join(dest_dir, image))
        counter +=1
        print("Processed", counter, "/", len(diff_files))
    