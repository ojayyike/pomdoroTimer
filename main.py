import time
import threading
import tkinter as tk
from tkinter import ttk, PhotoImage
import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
import vlc

class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x300")
        self.root.title("Pomodoro Timer ")
        self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file='images/timer.png'))
        
        self.s = ttk.Style()
        self.s.configure("TNotebook.Tab",font=("Franklin Gothic Medium", 16))
        self.s.configure("TButton",font=("Franklin Gothic Medium", 16))

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both",pady=10, expand=True)

        self.tab1 = ttk.Frame(self.tabs, width=600, height=400)
        self.tab2 = ttk.Frame(self.tabs, width=600, height=400)

        self.pomodoro_timer_label = ttk.Label(self.tab1, text="53:00", font=("Verdana",48))
        self.pomodoro_timer_label.pack(pady=20)

        self.break_timer_label= ttk.Label(self.tab2, text="17:00", font=("Verdana",48))
        self.break_timer_label.pack(pady=20)

        self.tabs.add(self.tab1, text="Pomodoro")
        self.tabs.add(self.tab2, text="Break")

        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=10)
        
        self.start_button = ttk.Button(self.grid_layout, text="Start", command=self.start_timer_thread)
        self.start_button.grid(row=0, column=0)

        self.reset_button= ttk.Button(self.grid_layout, text="Reset", command=self.reset_clock)
        self.reset_button.grid(row=0, column=1)
        
        self.pomodoro_counter_label = ttk.Label(self.grid_layout, text="Pomodoros: 0", font=("Verdana", 16))
        self.pomodoro_counter_label.grid(row=1,column=0,columnspan=3,pady=10)

        self.pomodoros = 0
        self.stopped = False
        self.running = False

        self.root.mainloop()
    def start_timer(self):
        self.stopped = False
        timer_id = self.tabs.index(self.tabs.select()) + 1
        if timer_id == 1:
            full_seconds = 60 * 53
            while full_seconds >= 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.pomodoro_timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            if not self.stopped:
                p = vlc.MediaPlayer("sounds/alarm.mp3")
                p.play()
                self.pomodoros += 1
                self.pomodoro_counter_label.config(text=f"Pomodoros: {self.pomodoros}")
                self.running = False
        elif timer_id == 2:
            full_seconds = 60 * 17
            while full_seconds >= 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.break_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            if not self.stopped:
                p = vlc.MediaPlayer("sounds/alarm.mp3")
                p.play()
                self.running = False
    def start_timer_thread(self):
        if not self.running: 
            t = threading.Thread(target=self.start_timer)
            t.start()
            self.running = True
    def reset_clock(self):
        self.stopped = True
        self.pomodoros = 0
        self.pomodoro_timer_label.config(text="53:00")
        self.break_timer_label.config(text="17:00")
        self.pomodoro_counter_label.config(text="Pomodoros: 0")
        self.running = False
PomodoroTimer()