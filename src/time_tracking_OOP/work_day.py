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

    def __str__(self):
        """Return a string representation of the work day."""
        return f"Work day: {self.day.strftime('%A %d %B %Y')}\nWeek No:  {self.day.strftime('%W')}"


    def start_work_day(self):
        """Start the work day."""
        self.work_start_time = datetime.datetime.now()


    def end_work_day(self):
        """End the work day."""
        self.work_end_time = datetime.datetime.now()


    def give_break(self):
        """Give a break during the work day."""
        self.break_count += 1
        self.latest_break = datetime.datetime.now()
        self.work_breaks[self.break_count] = {self.latest_break: None}


    def return_from_break(self):
        """Return from a break during the work day."""
        self.work_breaks[self.break_count][self.latest_break] = datetime.datetime.now()

    
    def count_break_time(self):
        """Count the time spent on breaks."""
        total_break_time = datetime.timedelta(0)
        for i in self.work_breaks.keys():
            for j in self.work_breaks[i].keys():
                if self.work_breaks[i][j] is not None:
                    total_break_time += self.work_breaks[i][j] - j
        self.total_break_time = total_break_time
        return self.total_break_time

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
            print(f"You have been working for {working_till}")
            return working_till

    def analyze_work_breaks(self):
        """Analyze the work breaks in human readable format."""
        for i in self.work_breaks.keys():
            for j in self.work_breaks[i].keys():
                if self.work_breaks[i][j] is not None:
                    return f"\tBreak {i} started at {j.strftime('%H:%M:%S')} and ended at {self.work_breaks[i][j].strftime('%H:%M:%S')}\n"
                else:
                    return f"\tBreak {i} started at {j.strftime('%H:%M:%S')} and is still ongoing.\n"

    def save_work_day(self):
        """Save the work day to a file."""
        pass

    def report_work_day(self):
        """Report the work day to the user in a txt file."""
        with open(f"{self.day.strftime('%d.%m.%Y')}_day_report.txt", 'w') as day_report:
            day_report.write(f"Work day: {self.day.strftime('%A %d %B %Y')}\nWeek No:  {self.day.strftime('%W')}\n\n")
            day_report.write(f"Work start: {self.work_start_time.strftime('%H:%M:%S')}\n")
            day_report.write(f"Work end: {self.work_end_time.strftime('%H:%M:%S')}\n")
            day_report.write(f"Total work time: {str(self.total_work_time).split('.')[0]}\n")
            day_report.write(f"Total break time: {str(self.total_break_time).split('.')[0]}\n")
            day_report.write(f"\nBreaks:\n {self.analyze_work_breaks()}\n")
        

