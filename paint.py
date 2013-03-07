 #A programe for GUI using TkInter for Takneek 2011 by Ankesh and Deepak

from Tkinter import *   #useful GUI functions
from tkColorChooser import askcolor
from PIL import Image, ImageTk
import tkFileDialog



class Painter :
  def __init__(self,parent) :
    self.myContainer1 = Frame(parent)  #create a main frame with  name myContainer1, it will contain all the widgets
    self.myContainer1.pack(fill= "both" , expand=1)  #fill says if user resize the window then resize the frame in both direction & expand tells the parent to assign                                                           additional space to widget box

    self.modes=[ PencilMode(), CircleMode(), RectangleMode()]
    self.colors='black'   # Default color
    self.cnt_mode=self.modes[0]

    self.cnt_data={'color':self.colors, 'width':1}
    #create menu bars at the top of all widgets
    menu=Menu(parent)  #create a menu
    root.config(menu=menu)

    #-------File Menu---------
    file_menu = Menu(menu)
    menu.add_cascade(label="File", menu=file_menu)   #sub-menu of main menu
    file_menu.add_command(label="New      Ctrl+N")      # menu option with name New
    file_menu.add_command(label="Open...  Ctrl+O", command =self.askopenfilename)
    file_menu.add_command(label="Save      Ctrl+S")
    file_menu.add_command(label="Save as")
    file_menu.add_command(label="Print      ctrl+P")
    file_menu.add_command(label="Recent")
    file_menu.add_separator()
    file_menu.add_command(label="Exit     Ctrl+Q",command= parent.quit)
    #----- Submenu of recent------
    # some codes-------
    #--------- End of File menu --------------


    #---------Edit Menu --------------
    Edit_menu=Menu(menu)
    menu.add_cascade(label="Edit", menu=Edit_menu)
    Edit_menu.add_command(label="Undo         Ctrl+Z")
    Edit_menu.add_command(label="Redo         Ctrl+R")
    Edit_menu.add_command(label="Copy         Ctrl+C")
    Edit_menu.add_command(label="Cut           Ctrl+X")
    Edit_menu.add_command(label="Clear")
    Edit_menu.add_command(label="Paste         Ctrl+V")
    Edit_menu.add_command(label="Select All   Ctrl+A")
    #----------End of edit menu-----------

    #------------Image menu----------------------------------------
    image_menu = Menu(menu)
    menu.add_cascade(label="Image", menu=image_menu)
    image_menu.add_command(label="Add Image")  #Import an image file
    image_menu.add_command(label="Rotate Clockwise")
    image_menu.add_command(label="Rotate Anticlockwise")
    image_menu.add_command(label="Resize imported Image")  
    #---------End of Image Menu--------------------------------------



    #---------Toolbars Menu------------------------------------------
    Toolbar_menu = Menu(menu)
    menu.add_cascade(label ="Toolbars" , menu= Toolbar_menu)
    Toolbar_menu.add_command(label="Crop")
    Toolbar_menu.add_command(label="Spray")
    Toolbar_menu.add_command(label="Blur")
    Toolbar_menu.add_command(label="Fill")
    Toolbar_menu.add_command(label="Random Shapes")
    Toolbar_menu.add_command(label="Modify")
    Toolbar_menu.add_command(label="Shapes" , command= self.shapes) 
 
    #---------End of Toolbars Menu-------------------------------
    #--------- Visual Effects---------
    Visual_menu=Menu(menu)
    menu.add_cascade(label ="Visual effect" , menu=Visual_menu)
    Visual_menu.add_command(label="Brightness")
    Visual_menu.add_command(label="Sharpness")
    Visual_menu.add_command(label="Hue")
    #----------help menu--------
    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu=helpmenu)
    helpmenu.add_command(label="Documentation")
    helpmenu.add_command(label="About...")
 
    #---------End of Help menu-------------------

    #------------ Create Canvas ---------------------------------------------------------------------------------------------------------------
    self.canvas=Canvas(self.myContainer1,height=400, width= 350, bg='white') # canvas is inside the main frame
    self.canvas.pack(fill="both" , expand =1) #canvas will adjust according to main frame
         #Bind drawing bindings to general handlers.
    self.canvas.bind("<Motion>", self.motion)
    self.canvas.bind("<ButtonPress-1>", self.b1down)
    self.canvas.bind("<ButtonRelease-1>", self.b1up)
      
  
#------------- Functions for changing color of lines---------------
  
    self.color_chooser = Button(self.myContainer1)
    self.color_chooser.configure(text="color", bg=self.colors,fg='white')
    self.color_chooser.pack(side=LEFT)
    self.color_chooser.bind("<Button-1>", self.colorset)
  

 #-----------Functions Related to width of line  
    self.width_l=Button(self.myContainer1)
    self.width_l.configure(text="Change Width")
    self.width_l.pack(side=LEFT)
    self.width_l.configure(command= self.scale)

  def update(self,width):      # update the value of width
    self.cnt_data['width']=width

  def scale(self):   # create a scale widget and configure button's command
    self.width=Scale(self.myContainer1,bd=0.5,width=7,length=200,orient = HORIZONTAL,resolution=0.5, from_=0, to=20, command =self.update)
    self.width.pack(expand = 1,side=LEFT)
    self.width_l.configure(command=self.scale_forget)
    
  def scale_forget(self):  #unpack the scale
    self.width.pack_forget()
    self.width_l.configure(command=self.scale)



  def colorset(self,event):  #changes the colorof lines
    (triple, hexstr) = askcolor()
    self.cnt_data['color']=hexstr
    self.color_chooser.configure(bg=self.cnt_data['color'])
#*************************************************************************

#------------------------
 
  def shapes(self) :  # A new window will open in which user will have to choose geometric shape mode
    
    self.top=Toplevel(master=self.myContainer1)
    self.top.title("Geometric Shapes")
   # self.lines=Button(self.top,text="Lines")
   # self.lines.pack()
   # self.splines=Button(self.top,text="SpLines")
   # self.splines.pack()
   # self.arc=Button(self.top,text="Arc")
   # self.arc.pack()
    
    self.mode_var=IntVar(self.top)                  # I don't know how it works but it works %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    for count in range(len(self.modes)):
      mode=self.modes[count]
      mode.button_args.update({'command':self.enter_mode, 'indicatoron':0, \
                               'variable':self.mode_var, 'value':count})
      mode.button=apply(Radiobutton, [self.top], mode.button_args)
      mode.button.pack(fill=X)


    #------------------------------- 
    


  def enter_mode(self):
    """Call the enter_mode fucntion of the mode itentified by the mode_var, and
    assign the new mode to the correct place; but only if the mode has changed."""
    new_mode=self.modes[self.mode_var.get()]
    if new_mode != self.cnt_mode:
    #  new_mode.enter_mode()
      self.cnt_mode=new_mode
#General Handlers:  They simply call the appropriete mode handlers.
  def b1down(self, event):
    self.cnt_mode.b1down(event, self.cnt_data)
  def b1up(self, event):
    self.cnt_mode.b1up(event, self.cnt_data)
  def motion(self, event):
    self.cnt_mode.motion(event, self.cnt_data)


  def askopenfilename(self):   # Ask user to give the path using dialog box

    

    #var=Image.open(filename)
    #logo=ImageTk.PhotoImage(var)
    #self.canvas.pack(image=logo) 
   

    filename=tkFileDialog.askopenfilename(filetypes=[("jpegfile","*.jpg"), ("pngfile","*.png"), ("giffile","*.gif")])

    gif1= ImageTk.PhotoImage( file= filename)
    myContainer1.canvas.create_image(50, 10, image = gif1, anchor = NW)


####################################################################
class GeneralMode:
  """The base class of all modes.  This includes empty defs of all used
  functions, so derived classes can ingore some of them without harm."""
  def __init__(self):
    pass
  def b1down(self, event):
    pass
  def b1up(self, event):
    pass
  def motion(self, event):
    pass
  def enter_mode(self):
    pass 
class RectangleMode(GeneralMode):
  def __init__(self):
    self.button_args={'text':'Rectangle'}
    self.btn='up'
    self.pt0=(None, None)
    self.pt1=(None, None)
  def b1down(self, event, data):
    self.btn='down'
    self.pt0=(event.x, event.y)
    event.widget.create_rectangle(event.x, event.y, event.x, event.y,\
                             tag='tmp_rect', outline=data['color'],\
                             width=data['width'])
  def motion(self, event, data):
    if self.btn=='down':
      event.widget.coords('tmp_rect', self.pt0[0], self.pt0[1],\
                          event.x, event.y)
  def b1up(self, event, data):
    self.btn='up'
    event.widget.dtag('tmp_rect', 'tmp_rect')

class PencilMode(GeneralMode):
  """Free drawing mode.  The basic code for this mode came from the old paint
  program of dave mitchell's."""
  def __init__(self):
    self.button_args={'text':'Pencil'}
    self.b1 = "up"
    self.xold = None
    self.yold = None
  def b1down(self, event, data):
    self.b1 = "down"   # you only want to draw when the button is down
                       # because "Motion" events happen -all the time-
  def b1up(self, event, data):
    self.b1 = "up"
    self.xold = None # reset the line when you let go of the button
    self.yold = None
  def motion(self, event, data):
    if self.b1 == "down":
      if self.xold != None and self.yold != None:
        # here's where you draw it. smooth. neat.
        event.widget.create_line(self.xold,self.yold,event.x,event.y,\
                                 smooth=TRUE, fill=data['color'], \
                                 width=data['width'])
      self.xold = event.x
      self.yold = event.y

class CircleMode(GeneralMode):
  """The first mode I created.  It creates one oval, then changes its coords
  till you let the mouse btn up."""
  def __init__(self):
    self.button_args={'text':'Circle'}
    self.btn='up'
    self.pt0=(None, None)
    self.pt1=(None, None)
  def b1down(self, event, data):
    self.btn='down'
    self.pt0=(event.x, event.y)
    event.widget.create_oval(event.x, event.y, event.x, event.y,\
                             tag='tmp_circle', outline=data['color'],\
                             width=data['width'])
  def motion(self, event, data):
    if self.btn=='down':
      event.widget.coords('tmp_circle', self.pt0[0], self.pt0[1],\
                          event.x, event.y)
  def b1up(self, event, data):
    self.btn='up'
    event.widget.dtag('tmp_circle', 'tmp_circle')




if __name__ == "__main__":
  root=Tk()
  it = Painter(root)
  root.title('Gand_Me_Danda')
  root.mainloop()

