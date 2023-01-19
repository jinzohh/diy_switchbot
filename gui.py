import tkinter
import tkinter.font as font
import subprocess, sys, os
import signal
import time
from datetime import datetime
from picamera import PiCamera

class Window(tkinter.Frame):

    def __init__(self, master=None):
        
        global pid #pid of server
        
        tkinter.Frame.__init__(self, master)
        
        self.master = master
        
        self.init_window()

        # open/close garage door option
        self.garageDoor_boolean = False

        # record option
        self.record_boolean = False

        # start/stop camera option
        self.camera_boolean = False
        self.camera = PiCamera()

        # server start by activating a script called server.py
        self.args = ['python3','server.py', 'arg1', 'arg2']
        self.proc = subprocess.Popen(self.args, shell=False)
        pid = self.proc.pid
        print(pid)
        self.poll = self.proc.poll()

def init_window(self):

    global button1
    global button2
    global button3

    self.master.title("Controller")

    self.pack(fill=tkinter.BOTH, expand=1)

    button1 = tkinter.Button(self, text="Start Recording", height = 5, width = 20, command=lambda: self.Record)
    button1.place(x=25, y=30)
    button1.bind('<ButtonRelease-1>', self.Record)

    button2 = tkinter.Button(self, text="Start Webcam", height = 5, width = 20, command=lambda: self.Webcam)
    button2.place(x=260, y=30)
    button2.bind('<ButtonRelease-1>', self.Webcam)

    button3 = tkinter.Button(self, text="Garage Door", height = 5, width = 20, command=lambda: self.Door)
    button3.place(x=150, y=200)
    button3.bind('<ButtonRelease-1>', self.Door)

def Door(self, event=None):

    # write to text file door.txt
    if(self.garageDoor_boolean == False):
        with open('door.txt', 'w') as f:
            f.write('1')
        self.garageDoor_boolean = True
    else:
        with open('door.txt', 'w') as f:
            f.write('0')
        self.garageDoor_boolean = False

def Record(self, event=None):

    self.camera.vflip = True
    self.camera.hflip = True

    if(self.record_boolean == False):
        timeStamp = datetime.now().strftime("%y%m%d_%H%M%S")
        self.camera.start_recording('/home/pi/Desktop/recordings/{}.h264'.format(timeStamp))
        self.record_boolean = True
        button1.config(text="Stop Recording")
    else:
        self.camera.stop_recording()
        self.record_boolean = False
        button1.config(text="Start Recording")

def Webcam(self, event=None):

    # No need to apply below if your camera is already right-side up
    self.camera.vflip = True
    self.camera.hflip = True

    if(self.camera_boolean == False):
        self.camera.start_preview(fullscreen=False, window=(-10, 100, 640, 480))
        self.camera_boolean = True
        button2.config(text="Stop Webcam")
    else:
        self.camera.stop_preview()
        self.camera_boolean = False
        button2.config(text="Start Webcam")

def closeWindow():

    # terminate server
    print(pid)
    proc_terminate = os.kill(pid, signal.SIGTERM)
    # close window
    root.destroy()

root = tkinter.Tk()

h = 420 # height of tk window

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

y = hs - h

root.geometry("480x400+0+%d" % (y))

app = Window(root)

root.protocol('WM_DELETE_WINDOW',closeWindow)

root.mainloop()