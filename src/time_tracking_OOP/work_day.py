"""WorkDay class"""

import datetime


class WorkDay:
    """A basic model for representing a work day"""

    def __init__(self):
        """Initialize the work day."""
        self.day = datetime.date.today()
        self.work_start_time = None
        self.work_end_time = None
        self.break_count = 0
        self.work_breaks = {}
        self.total_break_time = datetime.timedelta(0)
        self.latest_break = None
        self.total_work_time = None
        self.work_status = 'Not Started!'
        self.work_status_icons = {1: 'On Break!', 2: 'Working!', 3: 'Not Started!', 4: 'Day Ended!'}
        self.work_break_analysis = []

    def __str__(self):
        """Return a string representation of the work day."""
        return f"{self.day.strftime('%A')}\n{self.day.strftime('%d %B %Y')}\nWeek No: {self.day.strftime('%W')}"

    def get_day(self):
        """Return the day."""
        return self.day

    # Sets the work_start_time to the current time and sets the work_status to 'Working!'
    def start_work_day(self):
        """Start the work day."""
        self.work_start_time = datetime.datetime.now()
        self.work_status = self.work_status_icons[2]

    # Sets the work_end_time to the current time and sets the work_status to 'Day Ended!'
    def end_work_day(self):
        """End the work day."""
        self.work_end_time = datetime.datetime.now()
        self.work_status = self.work_status_icons[4]

    # Increments the break_count, sets the latest_break to the current time
    # Creates a work_breaks dictionary (break_count: None) and sets the work_status to 'On Break!'
    def give_break(self):
        """Give a break during the work day."""
        self.break_count += 1
        self.latest_break = datetime.datetime.now()
        self.work_breaks[self.break_count] = {self.latest_break: None}
        self.work_status = self.work_status_icons[1]

    # In work_breaks dictionary for the value of break_count key, sets another dictionary
    # key: latest_break value: current time
    def return_from_break(self):
        """Return from a break during the work day."""
        self.work_breaks[self.break_count][self.latest_break] = datetime.datetime.now()
        self.work_status = self.work_status_icons[2]

    # Creates a datetime.timedelta fucntion variable with value 0
    # Iterates through the work_breaks dictionary's keys
    # Iterates through again the inner dictionary
    # If the value of the inner dictionary is not None, adds the difference between the value and the key to the variable
    # Sets the total_break_time to the function variable
    def count_break_time(self):
        """Count the time spent on breaks."""
        total_break_time = datetime.timedelta(0)
        for i in self.work_breaks.keys():
            for j in self.work_breaks[i].keys():
                if self.work_breaks[i][j] is not None:
                    total_break_time += self.work_breaks[i][j] - j
        self.total_break_time = total_break_time
        return self.total_break_time

    # Checks if both work_start_time and work_end_time are not None
    # Sets the total_work_time to the count_break_time function calls return
    # If work_end_time are None, creates a now variable with the current time
    # Sets the working_till variable to the difference between now and work_start_time
    def count_work_time(self):
        """Count the time spent on work."""
        if self.work_start_time and self.work_end_time:
            total_break_time = self.count_break_time()
            self.total_work_time = self.work_end_time - self.work_start_time - total_break_time
            return self.total_work_time

        elif self.work_start_time and not self.work_end_time:
            total_break_time = self.count_break_time()
            now = datetime.datetime.now()
            working_till = now - self.work_start_time - total_break_time
            return working_till

    # Iterates through the work_breaks dictionary's keys
    # Iterates through again the inner dictionary
    # Checks the key,value of the inner dictionary
    # Add the information about breaks into the work_break_analysis list
    def analyze_work_breaks(self):
        """Analyze the work breaks in human readable format."""
        for i in self.work_breaks.keys():
            for j in self.work_breaks[i].keys():
                if self.work_breaks[i][j] is not None:
                    self.work_break_analysis.append(f"\tBreak {i} started at {j.strftime('%H:%M:%S')} and ended at {self.work_breaks[i][j].strftime('%H:%M:%S')}\n")
                else:
                    self.work_break_analysis.append(f"\tBreak {i} started at {j.strftime('%H:%M:%S')} and is still ongoing.\n")

    # Creates a txt file with the name format day.month.year_day_report.txt
    # Runs the count_work_time and count_break_time functions
    # Writes the work day information into the txt file e.g: day, work start time, etc.
    def report_work_day(self):
        """Report the work day to the user in a txt file."""
        self.count_work_time()
        self.count_break_time()
        with open(f"{self.day.strftime('%d.%m.%Y')}_day_report.txt", 'a') as day_report:
            day_report.write(f"{'#' * 55}\n")
            day_report.write(f"Work day: {self.day.strftime('%A %d %B %Y')}\nWeek No:  {self.day.strftime('%W')}\n\n")
            day_report.write(f"Work start: {self.work_start_time.strftime('%H:%M:%S')}\n")
            day_report.write(f"Work end: {self.work_end_time.strftime('%H:%M:%S')}\n")
            day_report.write(f"Total work time: {str(self.total_work_time).split('.')[0]}\n")
            day_report.write(f"Total break time: {str(self.total_break_time).split('.')[0]}\n")
            self.analyze_work_breaks()
            day_report.write("\nBreaks:\n")
            for i in self.work_break_analysis:
                day_report.write(i)
            day_report.write(f"{'#' * 55}\n")
