import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkcalendar as tkc
from datetime import datetime
from tkinter import messagebox


class DayStats(tk.Frame):

    def __init__(self, parent, user_info, daystats_day, current_database):
        parent.update()
        self.width = parent.winfo_width()
        self.height = parent.winfo_height()
        
        """Initialize window's attributes"""
        super().__init__(master=parent)
        self.parent = parent

        # current database
        self.current_database = current_database
        
        # current user using the app
        self.user_info = user_info
        
        # set the daystats_day to the WorkDay object passed in
        self.daystats_day = daystats_day
        # set the present_day to the current day
        self.present_day = self.daystats_day.day
        

        self.cal = tkc.Calendar(self, selectmode="day", year=self.present_day.year, month=self.present_day.month, day=self.present_day.day)
        self.cal.grid(row=0, column=1, columnspan=3, sticky=tk.NSEW)

        bar_chart_button = tk.Button(self, text="Bar Chart", command=lambda: self.show_bar_chart())
        bar_chart_button.grid(row=4, column=1, sticky=tk.NSEW)

        pie_chart_button = tk.Button(self, text="Pie Chart", command=lambda: self.show_pie_chart())
        pie_chart_button.grid(row=4, column=2, sticky=tk.NSEW)

        my_button = tk.Button(self, text="Get Date", command=self.grab_date)
        my_button.grid(row=4, column=3, sticky=tk.NSEW)


    def grab_date(self):
        # Get the date from the calendar
        requested_day = self.cal.get_date()
        formatted_date = datetime.strptime(requested_day, '%m/%d/%y').strftime('%Y-%m-%d')
        self.create_data_frame()
        

    def create_data_frame(self):
        # Create a pandas DataFrame to hold the data
        subject_day = datetime.strptime(self.cal.get_date(), '%m/%d/%y').strftime('%Y-%m-%d')
        subject_user = self.user_info
        subject_work_time = self.current_database.find_user_work_time(subject_user, subject_day)
        subject_break_time = self.current_database.find_user_break_time(subject_user, subject_day)
        
        # convert str time that is derived from the database to seconds (int)
        def convert_time_to_seconds(time):
            # Convert time to seconds
            time_list = time.split(':')
            second_convert_list = [3600, 60, 1]
            return sum([a*int(b) for a,b in zip(second_convert_list, map(int, time_list))])

        # create time objects for dataframe
        try:
            work_time = convert_time_to_seconds(subject_work_time)
            break_time = convert_time_to_seconds(subject_break_time)
        except:
            messagebox.showerror("Error", "No data for this day")

        self.df = pd.DataFrame({
            'Time': ['Work', 'Break'],
            'Length': [
                work_time,
                break_time
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


    def show_bar_chart(self):
        # Show the bar chart
        self.grab_date()
        self.create_bar_chart()

    
    def show_pie_chart(self):
        # Show the pie chart
        self.grab_date()
        self.create_pie_chart()


if __name__ == "__main__":
    app = DayStats()
    app.mainloop()