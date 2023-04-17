import tkinter as tk
import tkinter.ttk as ttk
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkcalendar as tkc
import work_day
import time_tracker

class DayStats(tk.Frame):

    def __init__(self, parent):
        parent.update()
        self.width = parent.winfo_width()
        self.height = parent.winfo_height()
        
        """Initialize window's attributes"""
        super().__init__(master=parent)
        self.parent = parent
        

        self.present_day = datetime.date.today()
        cal = tkc.Calendar(self, selectmode="day", year=self.present_day.year, month=self.present_day.month, day=self.present_day.day)
        cal.pack(pady=20)


        my_button = tk.Button(self, text="Get Date", command=self.grab_date)
        my_button.pack(pady=20)

        self.my_label = tk.Label(self, text="")
        self.my_label.pack(pady=20)

    def grab_date():
        self.my_label.config(text=cal.get_date())

        # Create a pandas DataFrame to hold the data
        self.df = pd.DataFrame({
            'Time': ['Work', 'Break'],
            'Length': [
                self.present_day.count_work_time().total_seconds() / 3600,
                self.present_day.count_break_time().total_seconds() / 3600
        ]
        })

    def create_bar_chart(self):
        # Create a bar chart of the work and break times
        fig, ax = plt.subplots()
        ax.bar(self.df['Time'], self.df['Length'])
        ax.set_xlabel('Time')
        ax.set_ylabel('Length (hours)')
        ax.set_title('Work and Break Times')
        plt.show()

    def create_pie_chart(self):
        # Create a pie chart of the total work and break times
        fig, ax = plt.subplots()
        ax.pie(self.df['Length'], labels=self.df['Time'], autopct='%1.1f%%')
        ax.set_title('Total Work and Break Times')
        plt.show()

if __name__ == "__main__":
    app = DayStats()
    app.mainloop()