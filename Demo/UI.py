# Copyright (c) 2019, Bosch Engineering Center Cluj and BFMC organizers
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
import tkinter as tk
from tkinter import ttk
from inspect import stack
from multiprocessing import Pipe
import cv2
from PIL import Image, ImageTk


class UI:
    """The graphical interface.

    Args:
        pipesend (multiprocessing.pipe.Pipe): pipe for sending the data
        piperecv (multiprocessing.pipe.Pipe): pipe for receiving the data
    """

    def __init__(self, pipesend, piperecv):
        self.root = tk.Tk()
        self.pipesend = pipesend
        self.piperecv = piperecv
        self.exitFlag = False
        self.started = False
        self.startedRecord = False
        self.create()

    def pause_main_loop(self, delay_ms):
        """Pause funtion

        Args:
            delay_ms (int): this will be the dealy in the quit function
        """
        self.root.after(delay_ms, self.root.quit)

    def create(self):
        """This will initialize the tkinter frame"""
        self.root.geometry("560x840")
        self.root.resizable(0, 0)
        Background = tk.Frame(self.root, background="white")
        Background.pack(fill="both", expand=True)
        self.root.bind("<KeyPress>", self.KeyPressEvent)

        # --------------------------------------------------------------------
        # -----------------------------Camera Frame---------------------------
        # --------------------------------------------------------------------

        self.CameraImg = tk.Label(
            self.root, image=ImageTk.PhotoImage(Image.open("img.jpg"))
        )
        self.CameraImg.place(x=55, y=285, height=360, width=480, in_=self.root)

        # --------------------------------------------------------------------
        # -----------------------------Speed Freame---------------------------
        # --------------------------------------------------------------------

        slider_label = tk.Label(
            self.root, text="Speed reference", background="white", borderwidth=0
        )
        slider_label.place(x=0, y=225, width=140, height=20, in_=self.root)
        PlusSpeed = tk.Button(self.root, text="+", command=self.plusSpeed)
        PlusSpeed.place(x=5, y=265, width=30, height=20, in_=self.root)
        self.Speedslider = tk.Scale(
            self.root,
            from_=50.0,
            to=-50.0,
            command=self.slidingSpeed,
            sliderlength=10,
            resolution=0.1,
        )
        self.Speedslider.place(x=5, y=285, width=50, height=360, in_=self.root)
        self.Speedslider.set(0.0)
        MinusSpeed = tk.Button(self.root, text="-", command=self.minusSpeed)
        MinusSpeed.place(x=5, y=645, width=30, height=20, in_=self.root)
        Brake = tk.Button(self.root, text="Brake", command=self.Brake)
        Brake.place(x=35, y=645, width=50, height=20, in_=self.root)

        # --------------------------------------------------------------------
        # -----------------------------Steering Frame-------------------------
        # --------------------------------------------------------------------

        slider_label = tk.Label(
            self.root, text="Steering reference", background="white", borderwidth=0
        )
        slider_label.place(x=230, y=220, width=140, height=20, in_=self.root)
        MinusSteer = tk.Button(self.root, text="-", command=self.minusSteer)
        MinusSteer.place(x=35, y=255, width=20, height=30, in_=self.root)
        self.Steerslider = tk.Scale(
            self.root, from_=-20, to=+20, orient="horizontal", command=self.slidingSteer
        )
        self.Steerslider.place(x=55, y=245, width=480, height=40, in_=self.root)
        self.Steerslider.set(0)
        PlusSteer = tk.Button(self.root, text="+", command=self.plusSteer)
        PlusSteer.place(x=535, y=255, width=20, height=30, in_=self.root)

        # --------------------------------------------------------------------
        # -----------------------------Control Frame---------------------------
        # --------------------------------------------------------------------
        self.labelSpeed = tk.Label(self.root, text="Speed:")
        self.labelSpeed.place(x=5, y=750, width=140, height=20, in_=self.root)
        self.text_box1 = tk.Text(self.root, width=40, height=20)
        self.text_box1.place(x=150, y=750, widt=140, height=20, in_=self.root)
        self.labelSteer = tk.Label(self.root, text="Steer:")
        self.labelSteer.place(x=5, y=780, width=140, height=20, in_=self.root)
        self.text_box2 = tk.Text(self.root, width=40, height=20)
        self.text_box2.place(x=150, y=780, widt=140, height=20, in_=self.root)
        self.labelTime = tk.Label(self.root, text="Time:")
        self.labelTime.place(x=5, y=810, width=140, height=20, in_=self.root)
        self.text_box3 = tk.Text(self.root, width=40, height=20)
        self.text_box3.place(x=150, y=810, widt=140, height=20, in_=self.root)
        button = tk.Button(self.root, text="Submit", command=self.SendCommand)
        button.place(x=295, y=750, width=260, height=80, in_=self.root)
        # --------------------------------------------------------------------
        # -----------------------------Start engine Frame---------------------
        # --------------------------------------------------------------------

        self.startEngineButton = tk.Button(
            self.root,
            text="Start engine",
            command=self.startEngine,
            background="red",
            state="disabled",
        )
        self.startEngineButton.place(x=5, y=665, width=275, height=80, in_=self.root)

        # --------------------------------------------------------------------
        # -----------------------------Start recording Frame---------------------
        # --------------------------------------------------------------------

        self.startRecordingButton = tk.Button(
            self.root,
            text="Start recording",
            command=self.startRecord,
            background="red",
            state="disabled",
        )
        self.startRecordingButton.place(
            x=280, y=665, width=275, height=80, in_=self.root
        )

        # --------------------------------------------------------------------
        # -----------------------------Topics Frame---------------------------
        # --------------------------------------------------------------------

        TopicsBox = tk.Frame(self.root, background="Yellow")
        TopicsBox.place(x=5, y=5, width=535, height=210, in_=self.root)

        self.my_game = ttk.Treeview(TopicsBox, selectmode="none")
        vsb = ttk.Scrollbar(self.root, orient="vertical", command=self.my_game.yview)
        vsb.place(x=540, y=5, height=210)

        self.my_game.configure(yscrollcommand=vsb.set)

        self.my_game["columns"] = ("Package", "Value")
        self.my_game["show"] = "headings"

        self.my_game.column("#0", width=0, stretch=tk.NO)
        self.my_game.column("Package", width=160)
        self.my_game.column("Value", anchor=tk.CENTER, width=375)

        self.my_game.heading("#0", text="", anchor=tk.CENTER)
        self.my_game.heading("Package", text="Package", anchor=tk.CENTER)
        self.my_game.heading("Value", text="Value", anchor=tk.CENTER)

        self.my_game.insert(parent="", index="end", iid=1, values=("IN_IMU", "pending"))
        self.my_game.insert(
            parent="", index="end", iid=2, values=("IN_LOCSYS_POS", "pending")
        )
        self.my_game.insert(
            parent="", index="end", iid=3, values=("IN_MOBILE_VEH", "pending")
        )
        self.my_game.insert(
            parent="", index="end", iid=4, values=("IN_SEMAPHORE", "pending")
        )
        self.my_game.insert(
            parent="", index="end", iid=5, values=("SYS_INSTANT_CON", "pending")
        )
        self.my_game.insert(
            parent="", index="end", iid=6, values=("SYS_BATTERY_LVL", "pending")
        )
        self.my_game.insert(
            parent="", index="end", iid=7, values=("SYS_ENGINE_OPE", "pending")
        )
        self.my_game.insert(
            parent="", index="end", iid=8, values=("SYS_ENGINE_RUN", "pending")
        )
        self.my_game.insert(
            parent="", index="end", iid=9, values=("RECORDING", "pending")
        )

        self.my_game.pack()
        self.root.update()

    # --------------------------------------------------------------------
    # --------------------------------------------------------------------
    # Speed section. Deals with everything that has to do with speed setup.
    # --------------------------------------------------------------------
    # --------------------------------------------------------------------

    def SendCommand(self):
        # Retrieve the text from the text boxes and store them in a dictionary
        text_dict = {
            "Speed": self.text_box1.get("1.0", "end-1c"),
            "Time": self.text_box3.get("1.0", "end-1c"),
            "Steer": self.text_box2.get("1.0", "end-1c"),
        }
        data = {"action": "STS", "value": text_dict}
        self.pipesend.send(data)
        print(data)

    def plusSpeed(self):
        """This function will increase the speed by 1"""
        speed = self.Speedslider.get() + 0.1
        if speed > 50:
            speed = 50
        self.setSpeed(speed)

    def minusSpeed(self):
        """This function will reduce the speed by 1"""
        speed = self.Speedslider.get() - 0.1
        if speed < -50:
            speed = -50
        self.setSpeed(speed)

    def slidingSpeed(self, val):
        self.setSpeed(val)

    def Brake(self):
        """This function will set the speed to 0"""
        self.setSpeed(0.0)
        data = {"action": "brake", "value": 0.0}
        self.pipesend.send(data)

    def setSpeed(self, val):
        """This function will send the speed

        Args:
            val (float): value to be changed
        """
        if not (
            stack()[1].function == "plusSpeed"
            or stack()[1].function == "minusSpeed"
            or stack()[1].function == "Brake"
        ):
            data = {"action": "speed", "value": val}
            self.pipesend.send(data)
        self.Speedslider.set(val)

    # --------------------------------------------------------------------
    # --------------------------------------------------------------------
    # Steering section. Deals with everything that has to do with steering setup.
    # --------------------------------------------------------------------
    # --------------------------------------------------------------------

    def plusSteer(self):
        """This function will increase the steering angle by 1"""
        steer = self.Steerslider.get() + 1.0
        if steer > 20.0:
            steer = 20.0
        self.setSteer(float(steer))

    def minusSteer(self):
        """This function will reduce the steering angle by 1"""
        steer = self.Steerslider.get() - 1.0
        if steer < -20.0:
            steer = -20.0
        self.setSteer(steer)

    def slidingSteer(self, val):
        self.setSteer(val)

    def setSteer(self, val):
        """This function will send the steering angle

        Args:
            val (float): value to be changed
        """
        if not (
            stack()[1].function == "plusSteer" or stack()[1].function == "minusSteer"
        ):
            data = {"action": "steer", "value": val}
            self.pipesend.send(data)
        self.Steerslider.set(val)

    # --------------------------------------------------------------------
    # --------------------------------------------------------------------
    # Starts the engine.
    # --------------------------------------------------------------------
    # --------------------------------------------------------------------

    def enableStartEngine(self, value):
        """This function will enable the start engine button."""
        if value == False:
            self.startEngineButton.config(state="disabled")
        else:
            self.startEngineButton.config(state="active")

    def enableStartRecord(self, value):
        """This function will enable the record button."""
        if value == False:
            self.startRecordingButton.config(state="disabled")
        else:
            self.startRecordingButton.config(state="active")

    def startEngine(self):
        """This function will swap the start engine button states."""
        if self.started:
            self.startEngineButton.config(background="green")
            self.startEngineButton.config(text="Start Engine")
            self.started = False
        else:
            self.startEngineButton.config(background="red")
            self.startEngineButton.config(text="Stop Engine")
            self.started = True

        data = {"action": "startEngine", "value": self.started}
        self.pipesend.send(data)

    def startRecord(self):
        """This function will swap the record button states."""
        if self.startedRecord:
            self.startRecordingButton.config(background="green")
            self.startRecordingButton.config(text="Start Record")
            self.startedRecord = False
        else:
            self.startRecordingButton.config(background="red")
            self.startRecordingButton.config(text="Stop Record")
            self.startedRecord = True

        data = {"action": "startRecord", "value": self.startedRecord}
        self.pipesend.send(data)

    # --------------------------------------------------------------------
    # --------------------------------------------------------------------
    # Keyboard functions for control.
    # --------------------------------------------------------------------
    # --------------------------------------------------------------------

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

    # --------------------------------------------------------------------
    # --------------------------------------------------------------------
    # Data fill.
    # --------------------------------------------------------------------
    # --------------------------------------------------------------------

    def emptyAll(self):
        for row_id in self.my_game.get_children():
            i, r = self.my_game.item(row_id)["values"]
            updated_values = (id, "pending")
            self.my_game.item(row_id, values=updated_values)

    def modifyTable(self, data):
        """This function will modify the table row if it already exists and it will ad a new raw if it doesn`t.

        Args:
            data (dictionary): A dictionary containing the id and the value.
        """
        id, value = data
        if self.root.winfo_exists():
            for row_id in self.my_game.get_children():
                i, r = self.my_game.item(row_id)["values"]
                if i == id:
                    updated_values = (id, value)
                    self.my_game.item(row_id, values=updated_values)
                    break
            else:
                ida = int(row_id) + 1
                self.my_game.insert(parent="", index="end", iid=ida, values=(id, value))

    def modifyImage(self, img):
        """This function will change the image displayed.

        Args:
            img (numpy array): this is the image that will be changed with.
        """
        try:
            img_np = cv2.imdecode(img, cv2.IMREAD_COLOR)
            pil_image = Image.fromarray(img_np)
            tk_image = ImageTk.PhotoImage(pil_image)
            self.CameraImg.config(image=tk_image)
            self.root.update()
        except Exception:
            print(Exception)
            self.root.update()

    def continous_update(self):
        """This function will always check if there is something on the pipe and will do the actions acordingly."""
        if self.piperecv.poll():
            msg = self.piperecv.recv()
            if msg["action"] == "modImg":
                self.enableStartRecord(True)
                self.modifyImage(msg["value"])
            elif msg["action"] == "enableStartEngine":
                self.enableStartEngine(msg["value"])
                self.modifyTable(["SYS_ENGINE_OPE", "True"])
            elif msg["action"] == "modTable":
                self.modifyTable(msg["value"])
            elif msg["action"] == "conLost":
                self.enableStartEngine(msg["value"])
                self.enableStartRecord(msg["value"])
                self.modifyTable(["SYS_ENGINE_OPE", "False"])
        self.root.after(0, self.continous_update)


if __name__ == "__main__":
    allProcesses = list()
    piperecv, pipesend = Pipe(duplex=False)
    piperecva, pipesenda = Pipe(duplex=False)
    server_thread = UI(pipesend)
    allProcesses.append(server_thread)

    print("Starting the processes!", allProcesses)
    for proc in allProcesses:
        proc.start()

    server_thread.root.mainloop()

    for proc in allProcesses:
        if hasattr(proc, "stop") and callable(getattr(proc, "stop")):
            print("Process with stop", proc)
            proc.stop()
            proc.join()
        else:
            print("Process witouth stop", proc)
            proc.terminate()
            proc.join()
