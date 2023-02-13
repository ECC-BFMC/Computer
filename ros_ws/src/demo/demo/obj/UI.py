from tkinter import *
from tkinter import ttk

from inspect import stack
import cv2

from PIL import Image, ImageTk

class UI():
    def __init__(self, speed, steer, engine):
        self.root = Tk() 
        self.sendSpeed = speed
        self.sendSteer = steer
        self.sendStartEngine = engine

    def create(self):
        self.root.geometry("790x300")
        self.root.resizable(0, 0)
        Background = Frame(self.root, background="blue")
        Background.pack( fill="both", expand=True)
        self.root.bind('<KeyPress>', self.KeyPressEvent)

        #--------------------------------------------------------------------
        #-----------------------------Camera Frame---------------------------
        #--------------------------------------------------------------------
        self.videoSize = (250,187)
        self.CameraImg = Label(self.root, width=self.videoSize[0], height=self.videoSize[1])
        self.CameraImg.place(x=175, y=100, in_=self.root)

        #--------------------------------------------------------------------
        #-----------------------------Speed Freame---------------------------
        #--------------------------------------------------------------------
        slider_label = Label(self.root, text='Speed reference', background="white", borderwidth=0)
        slider_label.place(x=5, y=100, width = 140, height = 20, in_=self.root)
        PlusSpeed=Button(self.root, text="+",command=self.plusSpeed)
        PlusSpeed.place(x=55, y=135, width = 30, height = 20, in_=self.root)
        self.Speedslider=Scale(self.root, from_=5.0, to=-5.0, command=self.slidingSpeed, sliderlength=10, resolution=0.1 )
        self.Speedslider.place(x=45, y=160, width = 50, height = 100, in_=self.root)
        self.Speedslider.set(0.0)
        MinusSpeed=Button(self.root, text="-",command=self.minusSpeed)
        MinusSpeed.place(x=55, y=265, width = 30, height = 20, in_=self.root)
        Brake=Button(self.root, text="Brake",command=self.Brake)
        Brake.place(x=100, y=200, width = 50, height = 20, in_=self.root)

        #--------------------------------------------------------------------
        #-----------------------------Steering Frame-------------------------
        #--------------------------------------------------------------------
        slider_label = Label(self.root, text='Steering reference', background="white", borderwidth=0)
        slider_label.place(x=230, y=5, width = 140, height = 20, in_=self.root)
        MinusSteer=Button(self.root, text="-",command=self.minusSteer)
        MinusSteer.place(x=175, y=45, width = 20, height = 30, in_=self.root)
        self.Steerslider=Scale(self.root,from_=-20, to=+20, orient="horizontal", command=self.slidingSteer)
        self.Steerslider.place(x=200, y=40, width = 200, height = 40, in_=self.root)
        self.Steerslider.set(0)
        PlusSteer=Button(self.root, text="+",command=self.plusSteer)
        PlusSteer.place(x=405, y=45, width = 20, height = 30, in_=self.root)

        #--------------------------------------------------------------------
        #-----------------------------Start engine Frame---------------------
        #--------------------------------------------------------------------
        self.startEngineButton=Button(self.root, text="Start engine",command=self.startEngine, background="red")
        self.startEngineButton.place(x=560, y=260, width = 100, height = 30, in_=self.root)

        #--------------------------------------------------------------------
        #-----------------------------Topics Frame---------------------------
        #--------------------------------------------------------------------
        TopicsBox = Frame(self.root, background="Yellow", width=200, height=300)
        TopicsBox.place(x=470, y=10, in_=self.root)
        
        self.my_game = ttk.Treeview(TopicsBox)
        self.my_game['columns'] = ('Package', 'Value')

        self.my_game.column("#0", width=0,  stretch=NO)
        self.my_game.column("Package", width=100)
        self.my_game.column("Value",anchor=CENTER,width=170)

        self.my_game.heading("#0",text="",anchor=CENTER)
        self.my_game.heading("Package",text="Package",anchor=CENTER)
        self.my_game.heading("Value",text="Value",anchor=CENTER)

        self.my_game.insert(parent='',index='end',iid=1,    values=('IN_IMU_ACC',   'pending'))
        self.my_game.insert(parent='',index='end',iid=2,    values=('IN_IMU_ROT',   'pending'))
        self.my_game.insert(parent='',index='end',iid=3,    values=('IN_LOC_POS',   'pending'))
        self.my_game.insert(parent='',index='end',iid=4,    values=('SYS_BAT_LVL',  'pending'))
        self.my_game.insert(parent='',index='end',iid=5,    values=('SYS_EN_OPE',   'pending'))
        self.my_game.insert(parent='',index='end',iid=6,    values=('SYS_EN_RUN',   'pending'))
        self.my_game.insert(parent='',index='end',iid=7,    values=('IN_MOB_VEH',   'pending'))
        self.my_game.insert(parent='',index='end',iid=8,    values=('IN_SEM_1',     'pending'))
        self.my_game.insert(parent='',index='end',iid=9,    values=('IN_SEM_2',     'pending'))
        self.my_game.insert(parent='',index='end',iid=10,   values=('IN_SEM_3',     'pending'))
        self.my_game.insert(parent='',index='end',iid=11,   values=('IN_SEM_4',     'pending'))
        

        self.my_game.pack()

    #--------------------------------------------------------------------
    #--------------------------------------------------------------------
    # Speed section. Deals with everything that has to do with speed setup.
    #--------------------------------------------------------------------
    #--------------------------------------------------------------------
    def plusSpeed(self):
        speed = self.Speedslider.get()+0.1
        if speed>5: speed=5
        self.setSpeed(speed)
    def minusSpeed(self):
        speed = self.Speedslider.get()-0.1
        if speed<-5: speed-5
        self.setSpeed(speed)
    def slidingSpeed(self, val):
        self.setSpeed(val)
    def Brake(self):
        self.setSpeed(0.0)

    def setSpeed(self, val):
        if not (stack()[1].function == "plusSpeed" or stack()[1].function =="minusSpeed" or stack()[1].function =="Brake"):
            self.sendSpeed(val)
        self.Speedslider.set(val)
                   

    #--------------------------------------------------------------------
    #--------------------------------------------------------------------
    # Steering section. Deals with everything that has to do with steering setup.
    #--------------------------------------------------------------------
    #--------------------------------------------------------------------
    def plusSteer(self):
        steer = self.Steerslider.get()+1
        if steer>20: steer=20
        self.setSteer(steer)
    def minusSteer(self):
        steer = self.Steerslider.get()-1
        if steer<-5: steer-5
        self.setSteer(steer)
    def slidingSteer(self, val):
        self.setSteer(val)

    def setSteer(self, val):
        if not (stack()[1].function == "plusSteer" or stack()[1].function =="minusSteer"):
            self.sendSteer(val)
        self.Steerslider.set(val)
        

    #--------------------------------------------------------------------
    #--------------------------------------------------------------------
    # Starts the engine.
    #--------------------------------------------------------------------
    #--------------------------------------------------------------------
    def startEngine(self):
        temp = self.startEngineButton.cget('bg')
        if temp =="red": 
            self.startEngineButton.config(background="green")
            started = True
        else: 
            self.startEngineButton.config(background="red")
            started = False

        self.sendStartEngine(started)

    #--------------------------------------------------------------------
    #--------------------------------------------------------------------
    # Keyboard functions for control.
    #--------------------------------------------------------------------
    #--------------------------------------------------------------------
    def KeyPressEvent(self, e):
        if e.keysym == "Up": 
            self.plusSpeed()
        elif e.keysym == "Down": 
            self.minusSpeed()
        elif e.keysym == "Right": 
            self.plusSteer()
        elif e.keysym == "Left": 
            self.minusSteer()
        elif e.keysym == "space": 
            self.Brake()

    def modifyTable(self, type, id, data):
        self.my_game.delete(id)
        self.my_game.insert(parent='',index=id-1 ,iid=id, values=(type, str(data)))

    def modifyImage(self, img):
        img = cv2.resize(img, self.videoSize)
        PILimg = Image.fromarray(img)
        background_image = ImageTk.PhotoImage(PILimg)
        self.CameraImg.configure(image = background_image)
        self.CameraImg.image = background_image

    def update(self):
        self.root.update()