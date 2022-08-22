from faulthandler import disable
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
from tkinter import DISABLED, NORMAL, filedialog as fd
import os
from PIL import Image
import numpy as np
from pathlib import Path
from tkinter import ttk

# from frontend import file_names

def file_names(file_path): 
        filename = file_path.split("/")[-1]
        return filename

def recolorization(dest_dir, file_paths):
    input_red = int(in_red.get())
    input_green = int(in_green.get())
    input_blue = int(in_blue.get())

    output_red = int(out_red.get())
    output_green = int(out_green.get())
    output_blue = int(out_blue.get())

    input_color = (input_red, input_green, input_blue)
    output_color = (output_red, output_green, output_blue)

    print(input_color)
    print(output_color)

    dest_folder = str(output_color)

    dest_dir = os.path.join(dest_dir, dest_folder)
    if os.path.exists(dest_dir):
        pass
    else:
        os.mkdir(dest_dir)

    #get recolorized files
    dest_files = os.listdir(dest_dir)

    #get diference between source and desti to avoid double processing
    diff_files = []

    for img in file_paths:
        file_name = img.split("/")[-1]
        if file_name in dest_files:
            pass
        else:
            diff_files.append(img)

    print(len(diff_files))

    #recolorize the imgs and save them to defualt folder
    if len(diff_files) == 0:
        l_processing_status["text"] = "no new files to recolorize..."
    else:
        counter = 0
        for image in diff_files:
            try:
                img = Image.open(image)
                image_name = image.split("/")[-1]

                # print(img.mode) #RGB
                # print(img.size)

                width = img.size[0] 
                height = img.size[1] 
                for i in range(0,width):# process all pixels
                    for j in range(0,height):
                        data = img.getpixel((i,j))
                        #print(data) #(255, 255, 255)
                        if (data[0]==input_red and data[1]==input_green and data[2]==input_blue):
                            img.putpixel((i,j),output_color)
                img.save(os.path.join(dest_dir, image_name))
                counter +=1
                status = "Processed " + str(counter) + "/" + str(len(diff_files))
                l_processing_status["text"] = status
                root.update()
            except:
                messagebox.showinfo(title="Error", message="An error occured on file %s. This image was not processed" % (image))
                l_processing_status["text"] = "Processing error"

        l_processing_status["text"] = "Processing done"
        
        path_ = os.path.realpath(dest_dir)
        os.startfile(path_)

class App(ttk.Frame):
    def __init__(self, root):
        ttk.Frame.__init__(self)

        #setting title
        root.title("Recolorizer")
        #setting window size
        width=600
        height=733
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        self.style= ttk.Style(self)

 
        GLabel_989=ttk.Label(root)
        ft = tkFont.Font(family='Calibri',size=22)
        GLabel_989["font"] = ft
        # GLabel_989["fg"] = "#333333"
        GLabel_989["justify"] = "center"
        GLabel_989["text"] = "Select files"
        GLabel_989.place(x=240,y=20,width=200,height=34)

        GButton_321=ttk.Button(root)
        # GButton_321["bg"] = "#f0f0f0"
        # ft = tkFont.Font(family='Calibri',size=10)
        # GButton_321["font"] = ft
        # GButton_321["fg"] = "#000000"
        # GButton_321["justify"] = "center"
        GButton_321["text"] = "Choose files"
        GButton_321.place(x=255,y=60,width=90,height=30)
        GButton_321["command"] = self.GButton_321_command

        global GListBox_478
        GListBox_478=tk.Listbox(root)
        GListBox_478["borderwidth"] = "1px"
        ft = tkFont.Font(family='Calibri',size=10)
        GListBox_478["font"] = ft
        GListBox_478["fg"] = "#333333"
        GListBox_478["justify"] = "left"
        GListBox_478.place(x=50,y=100,width=490,height=163)

        GLabel_244=tk.Label(root)
        ft = tkFont.Font(family='Calibri',size=10)
        GLabel_244["font"] = ft
        GLabel_244["fg"] = "#333333"
        GLabel_244["justify"] = "center"
        GLabel_244["text"] = "Source color  - RBG (0-255, 0-255, 0-255)"
        GLabel_244.place(x=50,y=290,width=250,height=30)

        GLabel_49=tk.Label(root)
        ft = tkFont.Font(family='Calibri',size=10)
        GLabel_49["font"] = ft
        GLabel_49["fg"] = "#333333"
        GLabel_49["justify"] = "right"
        GLabel_49["text"] = "R:"
        GLabel_49.place(x=50,y=330,width=70,height=30)

        GLabel_645=tk.Label(root)
        ft = tkFont.Font(family='Calibri',size=10)
        GLabel_645["font"] = ft
        GLabel_645["fg"] = "#333333"
        GLabel_645["justify"] = "right"
        GLabel_645["text"] = "G:"
        GLabel_645.place(x=50,y=360,width=70,height=33)

        GLabel_952=tk.Label(root)
        ft = tkFont.Font(family='Calibri',size=10)
        GLabel_952["font"] = ft
        GLabel_952["fg"] = "#333333"
        GLabel_952["justify"] = "right"
        GLabel_952["text"] = "B:"
        GLabel_952.place(x=50,y=390,width=70,height=30)

        global in_red
        in_red=tk.Entry(root)
        in_red["borderwidth"] = "1px"
        ft = tkFont.Font(family='Calibri',size=10)
        in_red["font"] = ft
        in_red["fg"] = "#333333"
        in_red["justify"] = "center"
        in_red.insert(0, "40")
        in_red.place(x=125,y=330,width=67,height=31)

        global in_green
        in_green=tk.Entry(root)
        in_green["borderwidth"] = "1px"
        ft = tkFont.Font(family='Calibri',size=10)
        in_green["font"] = ft
        in_green["fg"] = "#333333"
        in_green["justify"] = "center"
        in_green.insert(0, "40")
        in_green.place(x=125,y=360,width=67,height=30)

        global in_blue
        in_blue=tk.Entry(root)
        in_blue["borderwidth"] = "1px"
        ft = tkFont.Font(family='Calibri',size=10)
        in_blue["font"] = ft
        in_blue["fg"] = "#333333"
        in_blue["justify"] = "center"
        in_blue.insert(0, "40")
        in_blue.place(x=125,y=390,width=67,height=30)

        GLabel_93=tk.Label(root)
        ft = tkFont.Font(family='Calibri',size=10)
        GLabel_93["font"] = ft
        GLabel_93["fg"] = "#333333"
        GLabel_93["justify"] = "center"
        GLabel_93["text"] = "New Color - RBG (0-255, 0-255, 0-255)"
        GLabel_93.place(x=310,y=290,width=250,height=25)

        GLabel_367=tk.Label(root)
        ft = tkFont.Font(family='Calibri',size=10)
        GLabel_367["font"] = ft
        GLabel_367["fg"] = "#333333"
        GLabel_367["justify"] = "right"
        GLabel_367["text"] = "R:"
        GLabel_367.place(x=310,y=330,width=69,height=30)

        GLabel_777=tk.Label(root)
        ft = tkFont.Font(family='Calibri',size=10)
        GLabel_777["font"] = ft
        GLabel_777["fg"] = "#333333"
        GLabel_777["justify"] = "right"
        GLabel_777["text"] = "G:"
        GLabel_777.place(x=310,y=360,width=70,height=30)

        GLabel_813=tk.Label(root)
        ft = tkFont.Font(family='Calibri',size=10)
        GLabel_813["font"] = ft
        GLabel_813["fg"] = "#333333"
        GLabel_813["justify"] = "right"
        GLabel_813["text"] = "B:"
        GLabel_813.place(x=310,y=390,width=70,height=30)

        global out_red
        out_red=tk.Entry(root)
        out_red["borderwidth"] = "1px"
        ft = tkFont.Font(family='Calibri',size=10)
        out_red["font"] = ft
        out_red["fg"] = "#333333"
        out_red["justify"] = "center"
        out_red.insert(0, "167")
        out_red.place(x=380,y=330,width=73,height=30)
        
        global out_green
        out_green=tk.Entry(root)
        out_green["borderwidth"] = "1px"
        ft = tkFont.Font(family='Calibri',size=10)
        out_green["font"] = ft
        out_green["fg"] = "#333333"
        out_green["justify"] = "center"
        out_green.insert(0, "174")
        out_green.place(x=380,y=360,width=73,height=30)
        
        global out_blue
        out_blue=tk.Entry(root)
        out_blue["borderwidth"] = "1px"
        ft = tkFont.Font(family='Calibri',size=10)
        out_blue["font"] = ft
        out_blue["fg"] = "#333333"
        out_blue["justify"] = "center"
        out_blue.insert(0, "180")
        out_blue.place(x=380,y=390,width=73,height=30)

        GLabel_188=tk.Label(root)
        ft = tkFont.Font(family='Calibri',size=22)
        GLabel_188["font"] = ft
        GLabel_188["fg"] = "#333333"
        GLabel_188["justify"] = "center"
        GLabel_188["text"] = "Select output folder"
        GLabel_188.place(x=180,y=450,width=240,height=38)

        global GButton_536
        GButton_536=ttk.Button(root)
        # GButton_536["bg"] = "#f0f0f0"
        # ft = tkFont.Font(family='Calibri',size=10)
        # GButton_536["font"] = ft
        # GButton_536["fg"] = "#000000"
        # GButton_536["justify"] = "center"
        GButton_536["text"] = "Choose folder"
        GButton_536["state"] = DISABLED
        GButton_536.place(x=235,y=495,width=130,height=30)
        GButton_536["command"] = self.GButton_536_command

        GLabel_599=tk.Label(root)
        ft = tkFont.Font(family='Calibri',size=10)
        GLabel_599["font"] = ft
        GLabel_599["fg"] = "#333333"
        GLabel_599["justify"] = "center"
        GLabel_599["text"] = "Selected output path:"
        GLabel_599.place(x=230,y=535,width=140,height=30)


        global GLabel_775
        GLabel_775=tk.Label(root)
        ft = tkFont.Font(family='Calibri',size=10)
        GLabel_775["font"] = ft
        GLabel_775["fg"] = "#333333"
        GLabel_775["justify"] = "left"
        GLabel_775["text"] = ""
        GLabel_775.place(x=30,y=555,width=540,height=30)

        GLabel_342=tk.Label(root)
        ft = tkFont.Font(family='Calibri',size=22)
        GLabel_342["font"] = ft
        GLabel_342["fg"] = "#333333"
        GLabel_342["justify"] = "center"
        GLabel_342["text"] = "Recolorization"
        GLabel_342.place(y=600,width=598,height=25)

        global GButton_605
        GButton_605=ttk.Button(root)
        # GButton_605["bg"] = "#f0f0f0"
        # ft = tkFont.Font(family='Calibri',size=10)
        # GButton_605["font"] = ft
        # GButton_605["fg"] = "#000000"
        # GButton_605["justify"] = "center"
        GButton_605["text"] = "Start recolorization"
        GButton_605["state"] = DISABLED
        GButton_605.place(x=200,y=640,width=200,height=30)
        GButton_605["command"] = self.GButton_605_command

        global l_processing_status
        l_processing_status=tk.Label(root)
        ft = tkFont.Font(family='Calibri',size=10)
        l_processing_status["font"] = ft
        l_processing_status["fg"] = "#333333"
        l_processing_status["justify"] = "center"
        l_processing_status["text"] = ""
        l_processing_status.place(x=200,y=680,width=200,height=30)

    
    def GButton_321_command(self):
        print("select files")
        filetypes = (
            ('image files', '*.jpg'),
            ('image files', '*.jpeg'),
            ('image files', '*.png'),
            ('All files', '*.*')
        )
        global filenames

        filenames = fd.askopenfilenames(
            title='Open files',
            initialdir=r'C:\Users\Marek\Nextcloud2\_Logio (pro čtení)\Marketing\2. PIKTOGRAMY - RGB\black',
            filetypes=filetypes)
        print(filenames)

        GListBox_478.delete(0, tk.END)

        for x in filenames:
            filename = x #file_names(x)
            GListBox_478.insert(tk.END, filename + '\n')
        
        if len(filenames) > 0:
            GButton_536["state"] = NORMAL
        else:
            GButton_536["state"] = DISABLED


    def GButton_536_command(self):
        print("choose folder")
        global output_directory
        output_directory = fd.askdirectory()

        GLabel_775["text"] = output_directory
        if (len(filenames) > 0) and (output_directory != ""):
            GButton_605["state"] = NORMAL
        else:
            GButton_605["state"] = DISABLED



    def GButton_605_command(self):
        print("start recolorization")
        recolorization(output_directory, filenames)


if __name__ == "__main__":
    root = tk.Tk()

    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "light")
    app = App(root)
    root.mainloop()
