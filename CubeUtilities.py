import random
import datetime
import tkinter as tk


class CubeUtils:
    """Contains essential methods for a cube timer"""
    # Class variables
    LETTERS = ["R", "U", "L", "D", "F", "B"]
    WIDE_LETTERS = list(move.lower() for move in LETTERS)
    PUZZLE_TYPES = ["2x2", "3x3", "4x4", "5x5", "6x6", "7x7", "8x8", "9x9"]
    SCRAMBLE_LEN = 23
    QUALIFIERS = ["'", "2"]
    scramble = []

    @classmethod
    def generate_scramble(cls, length=23, puzzle_type="3x3") -> list:
        """
        Returns a randomly generated scramble with the length provided, default puzzle type is 3x3
        :param length: int
        :param puzzle_type: str
        :returns: list
        """
        cls.SCRAMBLE_LEN = length
        scramble = []

        for letter_index in range(cls.SCRAMBLE_LEN):
            # Generate a random letter

            if puzzle_type != "3x3" and puzzle_type != "2x2":
                # One in four chance of getting wide move

                wide_move = random.choice([False, False, False, True])

                if wide_move:
                    letter = random.choice(cls.WIDE_LETTERS)

                else:
                    letter = random.choice(cls.LETTERS)

            else:
                letter = random.choice(cls.LETTERS)

            if letter_index >= 2:
                if (
                        scramble[letter_index - 2].replace("'", "").replace("2", "")
                        == letter
                ):
                    # Make a copy of list without duplicate move and chose letter from that list
                    if puzzle_type != "3x3" and puzzle_type != "2x2":
                        letters = cls.LETTERS.copy() + cls.WIDE_LETTERS.copy()

                    else:
                        letters = cls.LETTERS.copy()

                    letters.remove(letter)

                    letter = random.choice(letters)

                if (
                        scramble[letter_index - 1].replace("'", "").replace("2", "")
                        == letter
                ):
                    # Make a copy of list without duplicate move and chose letter from that list
                    if puzzle_type != "3x3" and puzzle_type != "2x2":
                        letters = cls.LETTERS.copy() + cls.WIDE_LETTERS.copy()

                    else:
                        letters = cls.LETTERS.copy()

                    letters.remove(letter)

                    letter = random.choice(letters)

            elif letter_index == 1:
                # Check if previous move is the same as the current move

                if (
                        scramble[letter_index - 1].replace("'", "").replace("2", "")
                        == letter
                ):
                    # Make a copy of list without duplicate move and chose letter from that list
                    if puzzle_type != "3x3" and puzzle_type != "2x2":
                        letters = cls.LETTERS.copy() + cls.WIDE_LETTERS.copy()

                    else:
                        letters = cls.LETTERS.copy()

                    letters.remove(letter)

                    letter = random.choice(letters)

            # Chose randomly from True and False, if True then add a random qualifier to the current move
            qualifier = random.choice([True, False])

            if qualifier:
                letter += random.choice(cls.QUALIFIERS)

            # Add the move to the scramble
            scramble.append(letter)

        return scramble

    @classmethod
    def get_best_time(cls, times) -> int:
        """
        Returns the best time
        :param times: float[]
        :returns: float
        """
        if cls.find_DNFs(times):
            return "DNF"

        elif "DNF" in times:
            times_ = times.copy()
            times_.remove("DNF")
            return min(times_)

        else:
            best = min(times)
            return best

    @classmethod
    def get_worst_time(cls, times) -> int:
        """
        Returns the worst time
        :param times: float[]
        :returns: float
        """
        if "DNF" in times:
            return "DNF"

        worst = max(times)
        return worst

    @classmethod
    def find_DNFs(cls, times):
        """
        Returns True if there is times contains more than one DNF
        :param times: float[]
        :returns: bool
        """
        DNFS = {}
        for time in times:
            if time == "DNF" and len(DNFS) == 1:
                return True

            elif "DNF" in times:
                DNFS["DNF"] = True

        return False

    @classmethod
    def validate(cls, scramble) -> bool:
        """
        Returns True if scramble is valid, else, returns False
        :param scramble: char[]
        :return: bool
        """
        prev_move = scramble[0]
        for move in scramble[1: -1]:
            # Check if previous move is equal to current move
            if move == prev_move:
                return False

            prev_move = move

        return True

    @classmethod
    def check_for_pattern(cls, scramble) -> bool:
        """
        Checks scramble for any patterns, Returns True if there is a pattern
        :param scramble: char[]
        :return: boolean
        """
        prev_move = scramble[0]
        move = scramble[2]
        if prev_move == move:
            return False
        for move in scramble[2: -1]:
            prev_move = scramble[scramble.index(move) - 1]
            try:
                preceding = scramble[scramble.index(move) + 1]

            except IndexError:
                return False

            # Check if previous and preceding move are the same
            if prev_move == preceding:
                return True

        return False

    @classmethod
    def get_average(cls, times, ao=-1) -> float:
        """
        Returns average of times depending on ao parameter, defaulting to the whole list
        :param times: float[]
        :param ao: int
        :returns: float / str
        """
        for time in range(len(times)):
            if isinstance(times[time], str):
                times[time] = Time.convert_to_seconds(times[time])

        if len(times) == 0:
            return 0.0

        elif len(times) == 1:
            return times[0]

        if cls.find_DNFs(times):
            return "DNF"

        if ao == 12 and len(times) != 12:
            times_ = times[-12:-1]
            times_.append(times[-1])

        elif ao == 5 and len(times) != 5:
            times_ = times[-5:-1]
            times_.append(times[-1])

        elif ao == 100 and len(times) != 100:
            times_ = times[-100:-1]
            times_.append(times[-1])

        else:
            times_ = times.copy()

        if ao != -1:
            times_.remove(cls.get_best_time(times_))
            times_.remove(cls.get_worst_time(times_))

        elif ao == -1 and "DNF" in times_:
            return "DNF"

        for time in range(len(times_)):
            times_[time] = float(times_[time])

        try:
            average = round(float(sum(times_)) / len(times_), 2)
            if average > 59:
                average = Time.convert_to_minutes(average)
            return average

        except ZeroDivisionError:
            return 0.0


class Time:
    """Creates a time object that stores its time, scramble, date and whether or not it is a DNF"""
    def __init__(self, time, scramble, date, DNF=False):
        """
        :param time: float
        :param scramble: str
        :param date: datetime.datetime
        :param DNF; bool
        """
        if not isinstance(date, datetime.datetime):
            raise TypeError("date parameter must be of type datetime.datetime")

        if not isinstance(time, float):
            raise TypeError("time parameter must be of type float")

        if not isinstance(scramble, str):
            raise TypeError("scramble parameter must be of type str")

        if not isinstance(DNF, bool):
            raise TypeError("DNF parameter must be of type bool")

        self.time = time
        self.scramble = scramble
        self.date = datetime.datetime.strftime(date, "%Y-%m-%d-%I:%M %p")
        self.DNF = DNF

    @staticmethod
    def convert_to_seconds(time):
        """
        Converts the time to seconds, time must be equal to or greater than one minute
        :param time: str
        :returns: float
        """
        if not isinstance(time, str):
            raise TypeError("time argument must be of type str")

        if ":" in time:
            minutes = time.split(":")[0]
            seconds = time.split(":")[-1]
            if seconds[0] == "0":
                seconds = seconds[1: -1] + seconds[-1]

            time = str((float(minutes) * 60) + float(seconds))
            seconds = round(float(time), 2)

            return round(seconds, 2)

        return 0.0

    @staticmethod
    def convert_to_minutes(seconds):
        """
        Converts the seconds to minutes, time must be greater then 59 seconds and it must be a float
        :param seconds: float
        :returns: str
        """
        if not isinstance(seconds, float):
            raise TypeError("seconds argument must be of type float")

        elif seconds <= 59:
            return

        time = str(datetime.timedelta(seconds=seconds))
        time = time[2: -1] + time[-1]
        if time[0] == "0":
            time = time[1: -1] + time[-1]

        decimals = round(float("0." + time.split(".")[-1]), 2)
        decimals = str(decimals)[1: -1] + str(decimals)[-1]
        decimals = decimals.replace(".", "")
        old_decimals = time.split(".")[-1]

        time = time.replace(old_decimals, decimals)
        return time

    @staticmethod
    def plus_2(time):
        """
        Returns plus 2 of a time, time can be over 59 seconds
        :param time: float / str
        :return: float / str
        """

        # If time is less than a minute
        if isinstance(time, float):
            return round(time + 2, 2)

        # If time is over 59 seconds
        elif isinstance(time, str):
            time = Time.convert_to_seconds(time) + 2
            time = Time.convert_to_minutes(time)

            return time

        else:
            raise Exception("Time argument must be of type str or float.")

    def get_date(self, format="%Y-%m-%d-%I:%M %p"):
        """
        Returns the formatted date
        :param format: str
        :return: datetime.datetime
        """
        return datetime.datetime.strftime(self.date, format)

    def __str__(self):
        return f"{self.time}, {self.scramble}, {self.date}"


class MultiPhaseTime(Time):
    """Creates a Time object that stores a list of floats"""
    def __init__(self, times, *args, **kwargs):
        """
        :param times: List[float]
        """
        super().__init__(round(sum(times), 2), *args, **kwargs)

        self.times = times

    def get_times(self):
        """
        Returns the times list
        :return: List[float]
        """
        return self.times

    @staticmethod
    def convert_to_seconds(times):
        """
        Converts the sum of the list times to seconds
        :param times: List[float / str]
        :return: float
        """

        # Convert to float list
        float_times = times.copy()
        for index in range(len(float_times)):
            try:
                float_times[index] = Time.convert_to_seconds(float_times[index])

            except TypeError:
                pass

        time = sum(float_times)
        return Time.convert_to_seconds(time)

    @staticmethod
    def convert_to_minutes(seconds):
        """
        Converts the sum of the list times to minutes
        :param seconds: List[str / float]
        :return: str
        """

        # Convert to float list
        float_times = seconds.copy()
        for index in range(len(float_times)):
            try:
                float_times[index] = Time.convert_to_seconds(float_times[index])

            except TypeError:
                pass

        # Return sum of list in minutes
        time = sum(float_times)
        return Time.convert_to_minutes(time)

    @staticmethod
    def plus_2(times):
        """
        Returns the sum of times list, plus 2 seconds, time can be over 59 seconds
        :param times: List[float]
        """
        time = sum(times)
        if time > 59:
            time = Time.convert_to_minutes(time)

        return super().plus_2(time)


class TimeTable(tk.Frame):
    """Creates a time table using a tk.Canvas"""
    def __init__(self, parent, times, *args, **kwargs):
        """
        :param parent: tk.Tk()
        :param times: List[CubeUtils.Time]
        """

        # Initialize super class and define attributes
        super().__init__(*args, **kwargs)
        self.TIME_ATTRS = ["Time", "Scramble", "Date", "DNF"]
        self.fullscreen = False
        self.times = times
        self.canvas = tk.Canvas(self)
        self.frame = tk.Frame(self.canvas)
        self.parent = parent

        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.create_window(2, 2, window=self.frame, anchor="nw")

        # Bindings
        self.frame.bind("<Configure>", self.on_config)
        if len(self.times) >= 49:
            self.parent.bind("<MouseWheel>", self.on_mousewheel)

        self.parent.bind("<F11>", lambda event: self.toggle_fullscreen())
        self.parent.bind("<Escape>", lambda event: self.exit_fullscreen())

        # Populate frame
        self.populate()

    def populate(self):
        """Populates the frame with the times"""
        # Insert time attributes in text widgets
        for column, attr in enumerate(self.TIME_ATTRS):
            text = tk.Text(self.frame, font=("Arial", 15, "bold"), width=50, height=1)
            text.insert("0.0", attr)
            text.config(state=tk.DISABLED)
            column += 4
            text.grid(row=0, column=column)

        # Insert times in text widgets
        for time_count, time in enumerate(self.times):
            if time.time <= 59:
                time_info = [time_count + 1, time.time, time.scramble, time.date, time.DNF]

            else:
                time_info = [time_count + 1, Time.convert_to_minutes(time.time), time.scramble, time.date, time.DNF]

            time_info_font = ("Arial", 15, "bold")
            for column, info in enumerate(time_info):
                if isinstance(info, int) and not isinstance(info, bool):
                    text = tk.Text(self.frame, font=time_info_font, width=2 if len(str(info)) <= 2 else len(str(info)),
                                   height=1, fg="#ff5000")

                else:
                    text = tk.Text(self.frame, font=time_info_font, width=50, height=1, fg="#ff5000")

                text.insert("0.0", str(info))
                row = time_count + 1
                column += 3

                text.grid(row=row, column=column, sticky=tk.E)
                text.config(state=tk.DISABLED)

    def on_config(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        """Scrolls the canvas using the mouse wheel"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def toggle_fullscreen(self):
        """Toggles fullscreen on and off"""
        self.fullscreen = not self.fullscreen
        self.parent.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self):
        """Exists fullscreen"""
        self.fullscreen = False
        self.parent.attributes("-fullscreen", self.fullscreen)


def display_times(times):
    """
    Setups TimeTable object
    :param times: List[CubeUtils.Time]
    """
    root = tk.Tk()
    root.config(width=1000, height=1000)
    root.title("Time Table")
    time_table = TimeTable(root, times, height=1000, width=1000)
    time_table.pack(expand=True, fill=tk.BOTH)
    root.mainloop()


def generate_random_time():
    """
    Generates a time with a random time attribute and returns it
    :return: CubeUtils.Time
    """
    time = round(random.uniform(60.0, 120.0), 2)
    scramble = " ".join(CubeUtils.generate_scramble())
    date = datetime.datetime.now()
    time = Time(time, scramble, date)
    return time

def generate_random_DNF():
    """
    Generates a DNF time with a random time attribute and returns it
    :return: CubeUtils.Time
    """
    time = round(random.uniform(0.0, 30.0), 2)
    scramble = " ".join(CubeUtils.generate_scramble())
    date = datetime.datetime.now()
    time = Time(time, scramble, date, DNF=True)

    return time


if __name__ == "__main__":
    print (" ".join(CubeUtils.generate_scramble()))

