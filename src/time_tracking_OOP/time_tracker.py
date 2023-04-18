import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import simpledialog
#from PIL import Image, ImageTk
from pathlib import Path
from time import strftime
from datetime import date 
from userdatabase import UserDatabase


#import time_tracking_calendar 
from work_day import WorkDay
import day_stats

class TimeTracker(tk.Tk):
    """Time tracker main window"""

    def __init__(self):
        super().__init__()

        # root window
        self.title("Work Time Tracker ver 0.1.0")

        # window size and position
        self.geometry("%dx%d" % (self.winfo_screenwidth() * 3//5, self.winfo_screenheight() * 3//5))
    
        # bind close window event
        self.protocol("WM_DELETE_WINDOW", self.__close)
        
        # Show the the day information
        self.day = WorkDay()
        
        # Create the database for the user
        self.user_info = None
        self.database = UserDatabase()
        self.database.create_database()

        # create a pop up window to ask for player name
        self.player_login()

    # register a player
    def player_login(self):
            
        self.player_info = simpledialog.askstring("Input", "Welcome to Work Time Tracker. Please enter your name.")

        while self.player_info == "" or self.player_info == None:
            self.player_info = simpledialog.askstring("Input", "Welcome to Work Time Tracker. Please enter your name.")

        else:
            if self.database.find_user(self.player_info):
                messagebox.showinfo(title='Welcome Back', message=f'Hi, Welcome Back\n{self.player_info}')
                self.database.see_database()
            else:
                messagebox.showinfo(title='Welcome', message=f'Hi, Welcome\n{self.player_info}')
                self.database.add_user(self.player_info, date.today(),None, None)
                self.database.see_database()

        
        # Show the the day information
        self.work_day_label = ttk.Label(self, text=f"{self.day}", font=40)
        self.work_day_label.grid(row=0, column=0, sticky=tk.NSEW)

        # Show actual time
        self.time_label = ttk.Label(self, text="Time", font=40)
        self.time_label.grid(row=0, column=6, sticky=tk.NSEW)

        # Display Informaton about the current work day
        self.display_work_status()
        
        # Create buttons
        work_start_button = ttk.Button(self, text="Day Start", command=lambda: self.__start_work_day())
        work_start_button.grid(row=3, column=1, sticky=tk.NSEW)

        work_end_button = ttk.Button(self, text="Day End", command=lambda: self.__end_work_day())
        work_end_button.grid(row=3, column=4, sticky=tk.NSEW)

        break_button = ttk.Button(self, text="Give Break", command=lambda: self.__give_break())
        break_button.grid(row=3, column=2, sticky=tk.NSEW)

        return_button = ttk.Button(self, text="End Break", command=lambda: self.__end_break())
        return_button.grid(row=3, column=3, sticky=tk.NSEW)

        report_button = ttk.Button(self, text="Report Day", command=lambda: self.__report_work_day())
        report_button.grid(row=4, column=2, sticky=tk.NSEW)

        day_stats_button = ttk.Button(self, text="Day Stats", command=self.display_day_stats)
        day_stats_button.grid(row=4, column=3, sticky=tk.NSEW)

        self.columnconfigure((1,2,3,4,5), weight=1)
        self.rowconfigure((1,2,3,4,5), weight=1)
    
    # Show the actual time
    def show_time(self):
        time_string = strftime('%H:%M:%S') # time format 
        self.time_label.config(text=time_string)
        self.time_label.after(1000,app.show_time) # time delay of 1000 milliseconds 

    # Start the day
    def __start_work_day(self):
        """Start the work day."""
        self.day.start_work_day()
        self.display_work_status()

    # Give a break
    def __give_break(self):
        """Give a break."""
        self.day.give_break()
        self.display_work_status()

    # End the break
    def __end_break(self):
        """End the break."""
        self.day.return_from_break()
        self.display_work_status()
    
    # End the work day
    def __end_work_day(self):
        """End the work day."""
        self.day.end_work_day()
        self.display_work_status()
        self.database.add_work_time(self.player_info, date.today(), str(self.day.total_work_time).split('.')[0])
        self.database.add_break_time(self.player_info, date.today(), str(self.day.total_break_time).split('.')[0])

    # Report and save the work day
    def __report_work_day(self):
        """Report the work day."""
        self.day.report_work_day()
        self.database.add_work_time(self.player_info, date.today(), str(self.day.total_work_time).split('.')[0])
        self.database.add_break_time(self.player_info, date.today(), str(self.day.total_break_time).split('.')[0])
        self.database.see_database()

    # Display work status e.g: Working! or On Break!
    def display_work_status(self):
        """Display the current work status."""
        day_info_frame = ttk.Frame(self)
        self.work_status_label = ttk.Label(day_info_frame, text=f"{self.day.work_status}",font=100)
        self.work_status_label.pack(side=tk.TOP)
        day_info_frame.grid(row=2, column=2,columnspan=2, sticky=tk.NSEW)

    
    def display_day_stats(self):
        """Open day stats window and display stats for the work day."""
        window = tk.Toplevel(self)
        window.title("Day Stats")
        window.geometry("%dx%d" % (self.winfo_screenwidth() * 4//5, self.winfo_screenheight() * 4//5))
        window.update()
        home = day_stats.DayStats(window)
        home.pack(expand=True)
        home.grab_set()
        

    def __close(self):
        """Close window event"""
        if messagebox.askyesno("Quit", "Do you want to close the program?"):
            self.day.report_work_day()
            self.database.add_work_time(self.player_info, date.today(), str(self.day.total_work_time).split('.')[0])
            self.database.add_break_time(self.player_info, date.today(), str(self.day.total_break_time).split('.')[0])
            self.destroy()

if __name__ == "__main__":
    app = TimeTracker()
    app.show_time()
    app.mainloop()