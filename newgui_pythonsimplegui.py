#import modiles
import PySimpleGUI as sg
from PIL import Image
import numpy as np
from pathlib import Path
import os

#set theme of the app
sg.theme('Reddit')

#function to conver rgb to hex
def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

#function to conver filepaths string to filepaths list
def file_paths(paths):
    #get input from selection
    l_paths = paths.split(";")
    for f in l_paths:
        #check if the file was not already added (avoid duplicities in input)
        if not f in filepaths:
            filepaths.append(f)
        else:
            pass
    print("paths loaded")

    #get filenames to list them in inbox
    l_names = [f.split("/")[-1] for f in filepaths]
    for f in l_names:
        #get only image files
        if (f.lower().endswith((".png", ".gif", ".jpg", ".jpeg"))) and (f not in filenames):
            filenames.append(f)

#color check function
def color_check(r, g, b, color_list,boxes):
    #create reference list
    colors = {r:0, g:1, b:2}

    for i in [r,g,b]:

        if i!="":
            try:
                #convert to int - check if number
                val = int(i)
                #check if rgb correct
                if (val>=0) and (val<=255):
                    #remove highlight if correct
                    window[boxes[colors[i]]].Widget.configure(highlightcolor='red', highlightthickness=0)
                    color_list[colors[i]] = val
                else:
                    #add highlight if incorrect
                    window[colors[colors[i]]].Widget.configure(highlightcolor='red', highlightthickness=2)
                    #set alternative value for color
                    color_list[colors[i]] = 0
            except:
                #add highlight if incorrect
                window[boxes[colors[i]]].Widget.configure(highlightcolor='red', highlightthickness=2)
                #set alternative value for color
                color_list[colors[i]] = 0
        else:
            #add highlight if incorrect
            window[boxes[colors[i]]].Widget.configure(highlightcolor='red', highlightthickness=0)
            #set alternative value for color
            color_list[colors[i]] = 0


#check directory function
def check_dir(dir):
    #dont highlight if empty
    if dir != "":
        #remove highlight if correct
        if os.path.isdir(dir):
            window["-INOUTFOLDER-"].Widget.configure(highlightcolor='red', highlightthickness=0)

        else:
            #highlight if incorrect
            window["-INOUTFOLDER-"].Widget.configure(highlightcolor='red', highlightthickness=2)
    else:
        #dont highlight if empty
        window["-INOUTFOLDER-"].Widget.configure(highlightcolor='red', highlightthickness=0)


#check correcteness to start recolorization
def proces_start_check(in_files, out_folder):

    #check if input files are files and exist
    for file in in_files:
        if not os.path.isfile(file):
            sg.popup("Wrong file entered: %s" % {file})
            return False    

    #get in_color
    in_color = [values["-ININR-"],values["-INING-"],values["-ININB-"]]

    for i in in_color:
        try:
            # default value if empty
            if i =="":
                val = 0
            else:
                val = int(i)
            #check if rgb correct
            if (val>=0) and (val<=255):
                pass
            #return error if incorrect
            else:
                sg.popup("check input color")
                return False
        #return error if incorrect
        except:
            sg.popup("check input color")
            return False
    #get out color
    out_color = [values["-INOUTR-"],values["-INOUTG-"],values["-INOUTB-"]]

    for i in out_color:
        try:
            # default value if empty
            if i =="":
                val = 0
            else:
                val = int(i)
            #check if rgb correct
            if (val>=0) and (val<=255):
                pass
            #return error if incorrect
            else:
                sg.popup("check output color")
                return False
        #return error if incorrect
        except:
            sg.popup("check output color")
            return False
    #check if output dir exists
    if os.path.isdir(out_folder):
        pass
    #return error if incorrect
    else:
        sg.popup("Check output folder.")
        return False

    #if above correct start recolorization
    recolorization(in_color, out_color, filepaths, values["-INOUTFOLDER-"])


def recolorization(in_color, out_color, filepaths, out_folder):

    #invert in and out colors to ints
    in_color = [int(x) for x in in_color]

    out_color = [int(x) for x in out_color]

    out_color = tuple(out_color)
    print(in_color)
    print(out_color)
    
    #set and create output folder if rgb as folder name
    dest_folder = str(out_color)

    dest_dir = os.path.join(out_folder, dest_folder)
    if os.path.exists(dest_dir):
        pass
    else:
        os.mkdir(dest_dir)

    #get recolorized files
    dest_files = os.listdir(dest_dir)

    #get diference between source and destination to avoid double processing
    diff_files = []

    for img in filepaths:
        file_name = img.split("/")[-1]
        if file_name in dest_files:
            pass
        else:
            diff_files.append(img)

    print(len(diff_files))

    #recolorize the imgs and save them to defualt folder
    if len(diff_files) == 0:
        sg.popup( "no new files to recolorize...")
    else:
        counter = 0
        #recolorize each image
        for image in diff_files:
            try:
                #open image and get name
                img = Image.open(image)
                image_name = image.split("/")[-1]

                # print(img.mode) #RGB
                # print(img.size)
                #get height and with to process all pixels
                width = img.size[0] 
                height = img.size[1] 
                for i in range(0,width):# process all pixels
                    for j in range(0,height):
                        data = img.getpixel((i,j))
                        # version - change only defned color 
                        # if (data[0]==in_color[0] and data[1]==in_color[1] and data[2]==in_color[2]):
                        #     img.putpixel((i,j),out_color)
                        #version - everything but white background is recolorized
                        if (data[0]!=in_color[0] and data[1]!=in_color[1] and data[2]!=in_color[2]):
                            img.putpixel((i,j),out_color)
                #save image
                img.save(os.path.join(dest_dir, image_name))
                #increase counter and update progress text
                counter +=1
                status = "Processed " + str(counter) + "/" + str(len(diff_files))
                window["-TXTPROGRESS-"].update(status)
                window.refresh()
            #return error if error occures
            except:
                sg.popup("An error occured on file %s. This image was not processed" % (image))
                window["-TXTPROGRESS-"].update("Processing error")
        #update progress text after all images are processed
        window["-TXTPROGRESS-"].update("Processing done.")
        #automaticaly open file brower on output folder with new files
        path_ = os.path.realpath(dest_dir)
        os.startfile(path_)



#define global variables
filenames = [] #names of files to listbox
filepaths = [] #file paths to get images from drive

#input of in  and out colors, convet to list, tuple and set default hex 
in_boxes = {0:"-ININR-", 1:"-INING-", 2:"-ININB-"}
l_incolor = [0,0,0]
in_color = "#000"

out_boxes = {0:"-INOUTR-", 1:"-INOUTG-", 2:"-INOUTB-"}
l_outcolor = [0,0,0]
out_color = "#000"

#define layout
#select files frame
frame_selectFiles = [[sg.Text("Select source files", font=("Calibri", 20))],
                    [sg.FilesBrowse(key="-FILEBROWSER-",enable_events=True)],#sg.Button("Choose files", key="-BTNCHOOSEFILES-")],
                    [sg.Listbox(values=filenames,enable_events=True, size=(400,10),key="-LSTFILENAMES-")],
                    [sg.Button("Clear files", key="-BTNCLEARFILES-",enable_events=True)]
                    ]
#select colors
frame_selectInColors = [[sg.Text("Select origin color"), sg.Text("   ", background_color=in_color, key="-TXTINCOLOR-")],
                        [sg.Text("R: "), sg.In(key="-ININR-",default_text="40", enable_events=True, justification="center")],
                        [sg.Text("G: "), sg.In(key="-INING-",default_text="40", enable_events=True, justification="center")],
                        [sg.Text("B: "), sg.In(key="-ININB-",default_text="40", enable_events=True, justification="center")]                      
                        ]
frame_selectOutColors = [[sg.Text("Select new color"), sg.Text("   ", background_color=out_color, key="-TXTOUTCOLOR-")],
                        [sg.Text("R: "), sg.In(key="-INOUTR-", enable_events=True, justification="center")],
                        [sg.Text("G: "), sg.In(key="-INOUTG-", enable_events=True, justification="center")],
                        [sg.Text("B: "), sg.In(key="-INOUTB-", enable_events=True, justification="center")]
                        
                        ]

frame_completeColors = [[sg.Frame("In Color", layout=frame_selectInColors, size=(200,150), expand_x=True),sg.Frame("Out Color", layout=frame_selectOutColors, size=(200,150), expand_x=True)]]

#select output folder frame
frame_SelectOutFolder = [[sg.Frame("Output folder", layout= [[sg.Text("Select output folder", font=("Calibri", 20))],
                                                            [sg.In(key="-INOUTFOLDER-", enable_events=True),sg.FolderBrowse("Choose Folder", key="-BTNOUTFOLDER-")]
                                                            ]
                                    , expand_x=True, element_justification="center")]
                            
                            ]
 #start process frame
frame_StartRecolor = [[sg.Text("Start recolorization", font=("Calibri", 20))],
                        [sg.Button("Start process", key="-BTNSTART-", enable_events=True)],
                        [sg.Text("", key="-TXTPROGRESS-")]
                    ]

#layout definition
recolorizer_layout = [[sg.Column(layout=frame_selectFiles, element_justification='center')],
            [sg.Frame("Colors",layout=frame_completeColors, element_justification="center", expand_x=True)],
            [frame_SelectOutFolder],
            [frame_StartRecolor]
            ]
            


# window definition
window = sg.Window("Image Viewer", layout=recolorizer_layout, size=(600, 800), element_justification="center")

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    elif event == "-FILEBROWSER-":

        if values["-FILEBROWSER-"]: # check if files were selected, and get image files, update filepaths and filenames for listbox
            #create list of paths
            file_paths(values["-FILEBROWSER-"])

            window["-LSTFILENAMES-"].update(filenames) # updated listbox
            # print(filepaths, filenames)
    elif event == "-BTNCLEARFILES-": #clear selection and start over
        filenames = []
        filepaths= []
        window["-LSTFILENAMES-"].update(filenames)

    elif (event== "-ININR-") or (event== "-INING-") or (event== "-ININB-"):
        
        inred = values["-ININR-"]
        ingreen = values["-INING-"]
        inblue = values["-ININB-"]

        color_check(inred, ingreen, inblue, l_incolor,in_boxes) #check input of in_color values, and give preview 
        t_incolor = tuple(l_incolor)
        # print(rgb_to_hex(t_incolor))
        in_color = "#" + rgb_to_hex(t_incolor)
        # print(in_color)
        window["-TXTINCOLOR-"].update(background_color=in_color)

    elif (event== "-INOUTR-") or (event== "-INOUTG-") or (event== "-INOUTB-"): #check input of out_color values, and give preview 
        
        outred = values["-INOUTR-"]
        outgreen = values["-INOUTG-"]
        outblue = values["-INOUTB-"]

        color_check(outred, outgreen, outblue, l_outcolor, out_boxes)
        t_outcolor = tuple(l_outcolor)
        # print(rgb_to_hex(t_outcolor))
        out_color = "#" + rgb_to_hex(t_outcolor)
        # print(out_color)
        window["-TXTOUTCOLOR-"].update(background_color=out_color)

    elif event == "-INOUTFOLDER-": #get output folder and control correctness
        check_dir(values["-INOUTFOLDER-"])

    elif event == "-BTNSTART-":
        proces_start_check(filepaths,values["-INOUTFOLDER-"]) # start processing the files
        


window.close()