from tkinter import *
from tkinter.ttk import *
import idlelib.colorizer as ic
import idlelib.percolator as ip
import re
import sys
import easygui

name = None
saved = False

def more():

    details = """PiPy is an open source python IDE made by Desmond Vasicek (https://github.com/desvasicek).
PiPy was made for Raspberry Pi but can be used on any operating system.
If you wish to make commits or help this project, go to the github page for this project (https://github.com/desvasicek/pipy)

============================BASICS=======================================
CREATING AND RUNNING A PROJECT
- PiPy uses python, so see python docs for more information (https://www.python.org)
- To run a project, click "File" in the top left and then click "Run" in the dropdown
- To save a project click "File" in the top left and then click "Save" or "Save As".
        If you have already saved the file, then "Save" will save it to the file you have already set.
        "Save As" will always prompt for a new file name.
UNCAPABILITYS
- local modules, such as "C:\\users\\desvasicek\\project\\module.py" does not work with "import module"
"""
    console.config(state="normal")
    console.insert("end", "\n\n" + details)
    console.config(state="disabled")
def setunsaved(e):
    global name, saved
    saved = False
    if not name == None:
        pipy.title("PiPy - *" + name + "*")

def save():
    global name
    if not name:
        name = easygui.enterbox("File Name", "Please Enter File Name")
    file = open(name, mode="w")
    file.write(code.get("1.0", "end"))
    file.close()
    saved = True
    pipy.title("PiPy - " + name)

def save_as():
    global name
    name = easygui.enterbox("File Name", "Please Enter File Name")
    pipy.title("PiPy - " + name)
    file = open(name, mode="w")
    file.write(code.get("1.0", "end"))
    file.close()
    saved = True

def run():
    try:
        sys.stdout = open("test.txt", "w")
        exec(code.get("1.0", "end").replace("input(", "easygui.enterbox("))
        sys.stdout.close()
        printed_text = open("test.txt", "r").readlines()
        console.config(state="normal")
        console.insert("end", "\n\n" + "".join(printed_text))
        console.config(state="disabled")
    except Exception as e:
        printed_text = open("test.txt", "r").readlines()
        console.config(state="normal")
        console.insert("end", "\n\n" + "".join(printed_text) + "\n(" + str(e) +")")
        console.config(state="disabled")

def open_file():
    global name, saved
    saved = True
    file = easygui.fileopenbox("Choose File to Open", "Choose File")
    print(file)
    text = open(file, "r").read()
    path = file
    title = file.split("/")
    title = title[len(title) - 1]
    pipy.title("PiPy - " + title)
    console.config(state="normal")
    console.insert("end", "\n\nOpening " + title + "...")
    console.config(state="disabled")
    code.delete("1.0", "end")
    code.insert("1.0", text)
    name = title
def new_file():
    saveq = easygui.ynbox("Do you want to save this file?", "Save?")
    if saveq:
        save()
    name = None
    pipy.title("PiPy - *untitled*")
    code.delete("1.0", "end")
pipy = Tk()
pipy.geometry("900x900")
pipy.title("PiPy - *untitled*")
pipy.resizable(False, False)
menu = Menu()
file_menu = Menu(menu)
file_menu.add_command(label="Save", command=save)
file_menu.add_command(label="Save As", command=save_as)
file_menu.add_command(label="Run", command=run)
file_menu.add_separator()
file_menu.add_command(label="Quit", command=quit)
open_menu = Menu(menu)
open_menu.add_command(label="New", command=new_file)
open_menu.add_command(label="Open", command=open_file)
menu.add_cascade(label="Open", menu=open_menu)
menu.add_cascade(label="File", menu=file_menu)
pipy.config(menu=menu)
scroll = Scrollbar(pipy)
scroll.place(x=880, y=0, height=770, width=20)
code = Text(pipy, yscrollcommand=scroll.set)
code.place(x=0, y=0, width=880, height=770)
code.bind("<KeyRelease>", setunsaved)
scroll.config(command=code.yview)
console = Text(pipy, state='disabled')
console.place(x=0, y=770, width=900, height=130)
console.config(state="normal")
console.insert("1.0", """PiPy v1.0 on """ + sys.platform + """\nPiPy is a simple open source python-made Python IDE. Type "more()" for more information.""")
console.config(state="disabled")
try:
    name = sys.argv[1]
    saved = True
    code.insert("1.0", open(sys.argv[1]).read())
    pipy.title("PiPy - " + name)
    console.config(state="normal")
    console.insert("end", "\n\nOpening " + name + "...")
    console.config(state="disabled")
except Exception as e:
    console.insert("end", "\n\nOpening a new file...")
cdg = ic.ColorDelegator()
cdg.prog = re.compile(r'\b(?P<MYGROUP>tkinter)\b|' + ic.make_pat(), re.S)
cdg.idprog = re.compile(r'\s+(\w+)', re.S)
cdg.tagdefs['MYGROUP'] = {'foreground': '#7F7F7F', 'background': '#FFFFFF'}
cdg.tagdefs['COMMENT'] = {'foreground': '#FF0000', 'background': '#FFFFFF'}
cdg.tagdefs['KEYWORD'] = {'foreground': '#007F00', 'background': '#FFFFFF'}
cdg.tagdefs['BUILTIN'] = {'foreground': '#7F7F00', 'background': '#FFFFFF'}
cdg.tagdefs['STRING'] = {'foreground': '#7F3F00', 'background': '#FFFFFF'}
cdg.tagdefs['DEFINITION'] = {'foreground': '#007F7F', 'background': '#FFFFFF'}

ip.Percolator(code).insertfilter(cdg)

pipy.mainloop()

