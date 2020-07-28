from tkinter import *
import tkinter.scrolledtext as ScrolledText
from tkinter.filedialog import *
from tkinter.colorchooser import askcolor
import tkinter.messagebox
import os

from tkinter import simpledialog,messagebox


filename = None

def undo_command(event = None):
    try:
        text.edit_undo()
        lnupdater()
    except TclError:
        pass

def redo_command(event = None):
    try:
        text.edit_redo()
        lnupdater()
    except TclError:
        pass
def save_command(event = None):
    filename = asksaveasfilename(parent = root,defaultextension = '.txt',title = 'Save file as')
    if filename is not None:
        file = open(filename,mode = 'w')
        data = text.get('1.0',END)
        file.write(data)
        file.close()
        lnupdater()

def newFile(event=None):    #TO CREATE NEW FILE
    #global filename
    #filename="Untitled"
    #text.delete(0.0,END)
    if len(text.get('1.0',END+'-1c'))>0:
        if messagebox.askyesno("save?","Do you wish to save?"):
            saveAs()
        else:
            text.delete(0.0,END)
def cut(event=None):
    # first clear the previous text on the clipboard.
    root.clipboard_clear()
    text.clipboard_append(string=text.selection_get())
    #index of the first and yhe last letter of our selection.
    text.delete(SEL_FIRST, SEL_LAST)
def copy(event=None):                                                 # Copy Option

    text.clipboard_clear()

    text.clipboard_append(text.selection_get())
def paste(event=None):                                                #Paste Option

    try:

        teext = text.selection_get(selection='CLIPBOARD')

        text.insert(INSERT, teext)

    except:

        tkMessageBox.showerror("Errore","Gli appunti sono vuoti!")


def background():                    #Background Colour

    (triple,color) = askcolor()

    if color:

       text.config(background=color)
def findandreplace(event=None):                                                   #find and  Replace
    file = askopenfile(parent=root, mode='r+', title='Select a file')
    if file != None:
        contents = file.read()
        text.insert('1.0', contents)
        #file.close()
        search = find_replace()
        #enter2=tkinter.Label("Text to replace it with:")
        replaceme = replacetext()
        newdata = contents.replace(search,replaceme)
        f = open("test.txt",'w')
        f.write(newdata)
        text.delete(0.0,END)
        f.close()
        newfile=open("test.txt",'r+')
        contents1=newfile.read()
        text.insert('1.0',contents1)
def font():                            # TextColor                                

    (triple,color) = askcolor()

    if color:

       text.config(foreground=color)
def bold(event=None):                                #MAKE TEXT BOLD

    text.config(font = ("Arial", 12, "bold"))
def italic(event=None):                                      # MAKE TEXT ITALIC

    text.config(font = ("Arial",12,"italic"))

def bottom_bar():
    val = bbar.get()
    if val:
        bottombar.pack(expand = NO, fill = None, side = RIGHT, anchor = 'se')
    elif not val:
        bottombar.pack_forget()


def lnupdater(event = None):
    txt = ''
    el, ec = text.index('end-1c').split('.')
    txt = '\n'.join(map(str, range(1, int(el)+1)))
    cl, cc = text.index('insert').split('.')
    bottombar.config(text = 'Row : %s | Column: %s' %(cl,cc))
    #print "EL : ",el,"CL : ",cl
    if lc.get():
        lnc.pack(side = LEFT, anchor = 'nw', fill = Y)
        lnc.config(text = txt,anchor = 'nw')
    elif not lc.get():
        lnc.config(text = '',anchor = 'nw')

def lnupdatermouse(event):
    cl,cc = text.index(CURRENT).split('.')
    bottombar.config(text = 'Row : %s | Column: %s' %(cl,cc))
#def saveFile():  #TO SAVE FILE 
    
        

def saveAs():     # to saveas
    f=asksaveasfile(mode='w',defaultextension='.txt')
    t=text.get(0.0,END)
    try:
        f.write(t.rstrip())
    except:
        messagebox.showerror(title="OOPs",message="unable to save file ...")
def openFile():            #to open file
    try:
        f=askopenfile(mode='r',filetypes=(("Text File","*.txt"),("All Files","*.*")))
        t=f.read()
        text.delete(0.0,END)
        text.insert(0.0,t)
    except:
        pass

def highlight_line(interval = 100):
    text.tag_remove("active_line", 1.0, END)
    text.tag_add("active_line", "insert linestart", "insert lineend+1c")
    text.after(interval, toggle_highlight)

def undo_highlight():
    text.tag_remove("active line", 1.0, END)
    text.tag_configure("active_line", background = 'white')

def toggle_highlight(event = None):
    val = hltln.get()
    undo_highlight() if not val else highlight_line()


def col_sel_end(event=None, delete=0):
    try:
        start_index = textarea.index("sel.first").split(".")
        end_index = textarea.index("sel.last").split(".")
        start_line = int(start_index[0])
        start_char = int(start_index[1])
        end_line = int(end_index[0])
        end_char = int(end_index[1])
        text = ""
        counter = 0
        no_of_lines = end_line - start_line + 1
        while no_of_lines > 0:
            start_col_sel = str(start_line + counter) + "." + str(start_char)
            end_col_sel = str(start_line + counter) + "." + str(end_char)
            if delete == 1:
                textarea.delete(start_col_sel, end_col_sel)
            else:
                text = text + textarea.get( start_col_sel, end_col_sel ) + "\n"
            counter = counter + 1
            no_of_lines = no_of_lines - 1
        return text
    except TclError:
        textarea.tag_delete("selection")
        textarea.mark_set("insert", INSERT)
        
def col_sel_begin(event=None):
    textarea.bind("<ButtonRelease-1>", col_sel_end)
    textarea.tag_delete("selection")
    try:
        start_index = textarea.index("sel.first").split(".")
        end_index = textarea.index("sel.last").split(".")
        start_line = int(start_index[0])
        start_char = int(start_index[1])
        end_line = int(end_index[0])
        end_char = int(end_index[1])
        counter = 0
        no_of_lines = end_line - start_line + 1
        while no_of_lines > 0:
            start_line_char = str(start_line + counter) + "." + str(start_char)
            end_line_char = str(start_line + counter) + "." + str(end_char)
            textarea.tag_add("selection", start_line_char, end_line_char)
            no_of_lines = no_of_lines - 1
            counter = counter + 1
        textarea.tag_config("selection", background="blue", foreground="black")
    except TclError:
        textarea.mark_set("insert", INSERT)


def column_selection():
    if rs.get() == 1:
        textarea.config(selectbackground="white", inactiveselectbackground="white", selectforeground="black") 
        textarea.bind("<B1-Motion>", col_sel_begin)
    elif rs.get() == 0:
        textarea.unbind("<B1-Motion>")
        textarea.unbind("<ButtonRelease-1>")
        textarea.config(selectbackground="gray", inactiveselectbackground="white", selectforeground="black")

def drop_size(*args):                     #set font size
    txt = text.get(0.0,END)
    text.delete(0.0,END)
    text.configure(font = (text_style, var.get()))
    text.insert(0.0,txt)
    w.destroy()
def drop_style(*args):                  #set font style
    txt = text.get(0.0,END)
    text.delete(0.0,END)
    text.configure(font = (var.get(), text_size))
    text.insert(0.0,txt)
    w.destroy()

def font_style():           # defines option for font style
    global text, var, w
    var = StringVar(root)
    var.set(text_style)
    match_list = ["Times New Roman", "Helvetica", "Ariel", "Courier","Symbol"]
    var.trace('w', drop_style)
    w = OptionMenu(root, var, *match_list)
    w.pack()
def font_size():                  #provides option for font size
    global var, w
    var = StringVar(root)
    var.set(text_size)
    match_list = [8, 10, 11, 12, 14,16,24,28,30]
    var.trace('w', drop_size)
    w = OptionMenu(root, var, *match_list)
    w.pack()


root =Tk(className="Splash")


root.geometry('500x500')
lnc = Label(root,width = 2,bg = 'white')
lnc.pack(side = LEFT, anchor = 'nw', fill = Y)
text=ScrolledText.ScrolledText(root,width=200,height=200,font=("Arial", 10),undo = 1)  #This is actual text editor window
text.pack(fill="both",expand=True)
text_size = 10                           #defining text_size
text_style = "Arial"                     #defing text_style
menu = Menu(root) 
root.config(menu=menu) 

filemenu = Menu(menu,tearoff = 0) 
menu.add_cascade(label='File', menu=filemenu)     #FILE MENU
filemenu.add_command(label='New',command=newFile)   # options IN FILE MENU         
filemenu.add_command(label='Open',command=openFile) # options IN FILE MENU  
filemenu.add_command(label='Save',command=save_command) # options IN FILE MENU  
filemenu.add_command(label='SaveAS',command=saveAs)
 
filemenu.add_separator() 
filemenu.add_command(label='Exit', command=root.quit) #option in FILE MENU

editmenu=Menu(menu,tearoff = 0)
menu.add_cascade(label='Edit', menu=editmenu)
editmenu.add_command(label='Copy',command=copy,accelerator='Control+c')
editmenu.add_command(label='Cut',command=cut,accelerator='Control+x')  
editmenu.add_command(label='Paste',command=paste,accelerator='Control+v') 
editmenu.add_command(label='Background Color',command=background)# options IN FILE MENU 
editmenu.add_command(label='Text Color',command=font)
editmenu.add_command(label='Font Size',command=font_size)
editmenu.add_command(label='Font Style',command=font_style)


editmenu.add_command(label='Find and Replace',command=findandreplace,accelerator='Control+f')
editmenu.add_command(label='Bold',command=bold,accelerator='Control+b')
editmenu.add_command(label='Undo',command=undo_command,accelerator='Control+z')

editmenu.add_command(label='Redo',command=redo_command,accelerator='Control+y')

editmenu.add_command(label='Italic',command=italic,accelerator='Control+m')
lc = IntVar()
lc.set(1)
editmenu.add_checkbutton(label = "Display line numbers",onvalue = 1, offvalue = 0,variable = lc,command = lnupdater)
bbar = IntVar()
bbar.set(1)
editmenu.add_checkbutton(label = "Line and column information", onvalue = 1, offvalue = 0,variable = bbar, command = bottom_bar)

hltln = IntVar()
editmenu.add_checkbutton(label = "Highlight current line", onvalue = 1, offvalue = 0, variable = hltln, command = toggle_highlight)
rs = IntVar()
rs.set(0)
editmenu.add_checkbutton(label = "Column Selection",onvalue = 1, offvalue = 0,variable = rs,command = column_selection)



bottombar = Label(text, text = 'Row : 1 | Column : 0')
bottombar.pack(expand = NO, fill = None, side = RIGHT, anchor = 'se')    



text.tag_configure("active_line", background = "yellow")
text.bind("<Any-KeyPress>", lnupdater)
text.bind("<Button-1>", lnupdatermouse)

helpmenu = Menu(menu) 
menu.add_cascade(label='Help', menu=helpmenu) #HELP MENU
helpmenu.add_command(label='About')           #option in HELP Menu

def find_replace():                                                              # part of find and replace code
    find=simpledialog.askstring("Find and Replace","Enter the string to find ")
    return find
def replacetext():                                                               # part of find and replace code
    replacetext1 = simpledialog.askstring("Find and Replace", "Enter the string to replace")
    return replacetext1
root.config(menu=menu) 



def exit_editor(event=None):
    if tkinter.messagebox.askokcancel("Quit?", "Do you want to QUIT for sure?\n Make sure you've saved your current work."):
        root.destroy()
root.bind('<Control-q>', exit_editor)
root.bind('<Control-n>', newFile)
root.bind('<Control-o>', openFile)
#window.bind('<Control-s>', save_command)
root.bind('<Control-Shift-KeyPress-S>', saveAs)

root.bind('<Control-b>', bold)
root.bind('<Control-m>', italic)

root.bind('<Control-z>', undo_command)
root.bind('<Control-y>', redo_command)

root.bind('<Control-f>', findandreplace)




root.protocol('WM_DELETE_WINDOW', exit_editor)
root.mainloop()






