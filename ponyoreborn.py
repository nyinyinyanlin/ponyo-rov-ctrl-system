from Tkinter import *
import serial
from PIL import ImageTk, Image

class rov(object):
    def __init__(self):
        self.comm = serial.Serial()
        self.comm.baudrate = 9600

        self.imucomm = serial.Serial()
        self.imucomm.baudrate = 9600
        
        self.keyDict = {"w":False,"s":False,"a":False,"d":False,"i":False,"k":False,"j":False,"l":False}
        self.led1on = False
        self.led2on = False
        
        self.root = Tk()
        self.root.title("Ponyo Cockpit")
        
        self.frame = Frame(self.root)
        self.frame.pack()
        
        self.l1 = Label(self.frame,text="Serial COM")
        self.l1.grid(row=0,column=0,sticky=W)
        
        self.commEntry = Entry(self.frame)
        self.commEntry.grid(row=0,column=1)
        
        self.btnText = StringVar()
        self.btnText.set("Connect")
        self.b1 = Button(self.frame,textvariable=self.btnText,command=self.connectCOM)
        self.b1.grid(row=0,column=2)

        self.imuText = StringVar()
        self.imuText.set("Connect")
        self.b1 = Button(self.frame,textvariable=self.imuText,command=self.imuConnectCOM)
        self.b1.grid(row=1,column=2)
        
        self.l2 = Label(self.frame,text="Console:")
        self.l2.grid(row=1,column=0,sticky=W)
        self.consoleText = StringVar()
        self.consoleLabel = Label(self.frame,textvariable=self.consoleText)
        self.consoleLabel.grid(row=1,column=1,columnspan=1)
        self.consoleText.set("Konichiwa!")
        
        self.tempL = Label(self.frame,text="Temperature(Celcius)-")
        self.tempL.grid(row=2,column=0,sticky=W)
        self.tempVar = StringVar()
        self.tempLabel = Label(self.frame,textvariable=self.tempVar)
        self.tempLabel.grid(row=2,column=1,columnspan=1)
        
        self.pressL = Label(self.frame,text="Pressure(kPa)-")
        self.pressL.grid(row=3,column=0,sticky=W)
        self.pressVar = StringVar()
        self.pressLabel = Label(self.frame,textvariable=self.pressVar)
        self.pressLabel.grid(row=3,column=1,columnspan=1)
        
        self.depthL = Label(self.frame,text="Depth(m)-")
        self.depthL.grid(row=4,column=0,sticky=W)
        self.depthVar = StringVar()
        self.depthLabel = Label(self.frame,textvariable=self.depthVar)
        self.depthLabel.grid(row=4,column=1,columnspan=1)
                                                    
        self.yawL = Label(self.frame,text="Yaw(N)-")
        self.yawL.grid(row=5,column=0,sticky=W)
        self.yawVar = StringVar()
        self.yawLabel = Label(self.frame,textvariable=self.yawVar)
        self.yawLabel.grid(row=5,column=1,columnspan=1)
        self.yawDeg = 0
        self.yawCanvas = Canvas(self.frame, width=240, height=120)
        self.yawCanvas.grid(row=6,column=0,columnspan=3,sticky=W)
        self.yawImg = Image.open('yaw.png')
        self.yawImg.load()
        self.yawCanvas.image = ImageTk.PhotoImage(self.yawImg)
        self.yawCanvasImg = self.yawCanvas.create_image(120, 60, image=self.yawCanvas.image, anchor=CENTER)
        self.yawTempImg = None
        
        self.rollL = Label(self.frame,text="Roll(Deg)-")
        self.rollL.grid(row=7,column=0,sticky=W)
        self.rollVar = StringVar()
        self.rollLabel = Label(self.frame,textvariable=self.rollVar)
        self.rollLabel.grid(row=7,column=1,columnspan=1)
        self.rollDeg = 0
        self.rollCanvas = Canvas(self.frame, width=240, height=120)
        self.rollCanvas.grid(row=8,column=0,columnspan=3,sticky=W)
        self.rollImg = Image.open('roll.png')
        self.rollImg.load()
        self.rollCanvas.image = ImageTk.PhotoImage(self.rollImg)
        self.rollCanvasImg = self.rollCanvas.create_image(120, 60, image=self.rollCanvas.image, anchor=CENTER)
        self.rollTempImg = None
        
        self.pitchL = Label(self.frame,text="Pitch(Deg)-")
        self.pitchL.grid(row=9,column=0,sticky=W)
        self.pitchVar = StringVar()
        self.pitchLabel = Label(self.frame,textvariable=self.pitchVar)
        self.pitchLabel.grid(row=9,column=1,columnspan=1)
        self.pitchDeg = 0
        self.pitchCanvas = Canvas(self.frame, width=240, height=120)
        self.pitchCanvas.grid(row=10,column=0,columnspan=3,sticky=W)
        self.pitchImg = Image.open('pitch.png')
        self.pitchImg.load()
        self.pitchCanvas.image = ImageTk.PhotoImage(self.pitchImg)
        self.pitchCanvasImg = self.pitchCanvas.create_image(120, 60, image=self.pitchCanvas.image, anchor=CENTER)
        self.pitchTempImg = None
        
        self.led1btn = Button(self.frame,text="LED1 ON",command=self.toggleLed1)
        self.led2btn = Button(self.frame,text="LED2 ON",command=self.toggleLed2)
        self.led1btn.grid(row=2,column=2)
        self.led2btn.grid(row=3,column=2)

        self.root.bind_all('<KeyPress>', self.keypress)
        self.root.bind_all('<KeyRelease>', self.keyrelease)
        self.root.bind("<Button-1>",self.click)
        
        self.root.after(10,self.pgm)
        self.root.mainloop()

    def connectCOM(self):
        if self.comm.isOpen():
            self.consoleText.set(self.commEntry.get()+": Disconnected")
            self.btnText.set("Connect")
            self.comm.close()
        else:
            try:
                self.comm.port = self.commEntry.get()
                self.comm.open()
            except serial.SerialException:
                self.consoleText.set(self.commEntry.get()+": Error connecting")
                self.btnText.set("Connect")
            else:
                self.consoleText.set(self.commEntry.get()+": Successfully connected")
                self.btnText.set("Disconnect")
        self.frame.focus()
        
    def imuConnectCOM(self):
        if self.imucomm.isOpen():
            self.consoleText.set(self.commEntry.get()+": IMU disconnected")
            self.imuText.set("Connect")
            self.imucomm.close()
        else:
            try:
                self.imucomm.port = self.commEntry.get()
                self.imucomm.open()
            except serial.SerialException:
                self.consoleText.set(self.commEntry.get()+": Error connecting IMU")
                self.imuText.set("Connect")
            else:
                self.consoleText.set(self.commEntry.get()+": IMU connected")
                self.imuText.set("Disconnect")
        self.frame.focus()

    def pgm(self):
        if self.comm.isOpen() and self.comm.inWaiting():
            data = self.comm.readline()
            identifier = data[0]
            data = data[1:len(data)-1]
            if identifier == 'P':
                self.pressVar.set(data)
            elif identifier == 'T':
                self.tempVar.set(data)
            elif identifier == 'D':
                self.depthVar.set(data)
            elif identifier == 'c':
                self.consoleText.set(data)
        if self.imucomm.isOpen() and self.imucomm.inWaiting():
            data = self.imucomm.readline()
            identifier = data[0]
            data = data[1:len(data)-1]
            if identifier == 'y':
                self.yawVar.set(180-float(data))
                self.yawDeg = 180-float(data)
                self.updateYaw()
            elif identifier == 'p':
                self.pitchVar.set((-1)*float(data))
                self.pitchDeg = (-1)*float(data)
                self.updatePitch()
            elif identifier == 'R':
                self.rollVar.set(data)
                self.rollDeg = float(data)
                self.updateRoll()
        self.root.after(10,self.pgm)

    def updateYaw(self):
        self.yawTempImg = ImageTk.PhotoImage(self.yawImg.rotate(int(self.yawDeg),resample=Image.BICUBIC))
        self.yawCanvas.itemconfig(self.yawCanvasImg,image=self.yawTempImg)

    def updateRoll(self):
        self.rollTempImg = ImageTk.PhotoImage(self.rollImg.rotate(int(self.rollDeg),resample=Image.BICUBIC))
        self.rollCanvas.itemconfig(self.rollCanvasImg,image=self.rollTempImg)

    def updatePitch(self):
        self.pitchTempImg = ImageTk.PhotoImage(self.pitchImg.rotate(int(self.pitchDeg),resample=Image.BICUBIC))
        self.pitchCanvas.itemconfig(self.pitchCanvasImg,image=self.pitchTempImg)
        
    def sendCmd(self,cmd):
        if self.comm.isOpen():
            cmd = cmd + "t"
            self.comm.write(cmd)
            self.comm.flush()

    def keypress(self,event):
        key = event.char
        if event.widget is not self.commEntry:
            if key in self.keyDict:
                if not self.keyDict[key]:
                    self.keyDict[key] = True
                    self.mtrStart(key)
            else:
                if key is "q":
                    self.toggleLed1()
                elif key is "e":
                    self.toggleLed2()
                
    def keyrelease(self,event):
        key = event.char
        if event.widget is not self.commEntry:
            if key in self.keyDict:
                if self.keyDict[key]:
                    self.keyDict[key] = False
                    self.mtrStop(key)

    def click(self,event):
        if event.widget is not self.commEntry:
            self.frame.focus()
        else:
            self.commEntry.focus()

    def mtrStart(self,key):
         if key == "w":
             self.sendCmd("f1")
         elif key == "s":
             self.sendCmd("b1")
         elif key == "a":
             self.sendCmd("l1")
         elif key == "d":
             self.sendCmd("r1")
         elif key == "i":
             self.sendCmd("u1")
         elif key == "k":
             self.sendCmd("d1")
         elif key == "j":
             self.sendCmd("a1")
         elif key == "l":
             self.sendCmd("c1")
             
    def mtrStop(self,key):
          if key == "w":
             self.sendCmd("f0")
          elif key == "s":
             self.sendCmd("b0")
          elif key == "a":
             self.sendCmd("l0")
          elif key == "d":
             self.sendCmd("r0")
          elif key == "i":
             self.sendCmd("u0")
          elif key == "k":
             self.sendCmd("d0")
          elif key == "j":
             self.sendCmd("a0")
          elif key == "l":
             self.sendCmd("c0")

    def toggleLed1(self):
        if self.comm.isOpen():
            if self.led1on:
                self.sendCmd("v0")
                self.led1on = False
                self.led1btn.config(text="LED1 ON")
            else:
                self.sendCmd("v1")
                self.led1on = True
                self.led1btn.config(text="LED1 OFF")
                
    def toggleLed2(self):
        if self.comm.isOpen():
            if self.led2on:
                self.sendCmd("g0")
                self.led2on = False
                self.led2btn.config(text="LED2 ON")
            else:
                self.sendCmd("g1")
                self.led2on = True
                self.led2btn.config(text="LED2 OFF")

rov()
