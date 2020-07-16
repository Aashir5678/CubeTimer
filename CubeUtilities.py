import random
import datetime


class CubeUtils:
    # Class variables
    LETTERS = ["R", "U", "L", "D", "F", "B"]
    SCRAMBLE_LEN = 23
    QUALIFIERS = ["'", "2"]
    scramble = []

    @classmethod
    def generate_scramble(cls, length=23) -> list:
        """
        Returns a randomly generated scramble
        :param int length: length of scramble
        :returns: list
        """
        # Making scramble list and setting scramble length
        cls.SCRAMBLE_LEN = length
        scramble = []

        for letter_index in range(cls.SCRAMBLE_LEN):
            # Generate a random letter
            letter = random.choice(cls.LETTERS)
            if letter_index >= 2:
                if (
                    scramble[letter_index - 2].replace("'", "").replace("2", "")
                    == letter
                ):
                    # Make a copy of list without duplicate move and chose letter from that list
                    letters = cls.LETTERS.copy()

                    letters.remove(letter)

                    letter = random.choice(letters)

                if (
                    scramble[letter_index - 1].replace("'", "").replace("2", "")
                    == letter
                ):
                    # Make a copy of list without duplicate move and chose letter from that list
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
        :param times: list
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
        :param times: list
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
        :param times: list
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
        :param scramble: list
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
        :param scramble: list
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
        :param times: list
        :param ao: int
        :returns: float / str
        """
        for time in range(len(times)):
            if isinstance(times[time], str):
                times[time] = Time.convert_seconds(times[time])

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
                average = Time.convert_minutes(average)
            return average

        except ZeroDivisionError:
            return 0.0


class Time:
    def __init__(self, time, scramble, date, DNF=False):
        """
        :param time: float
        :param scramble: str
        :param date: datetime.datetime
        :param DNF; bool
        """
        if not isinstance(date, datetime.datetime):
            raise TypeError("date parameter must be of type datetime.datetime")

        self.time = time
        self.scramble = scramble
        self.date = datetime.datetime.strftime(date, "%Y-%m-%d-%I:%M %p")
        self.DNF = DNF

    @staticmethod
    def convert_seconds(time):
        """
        Converts the time to seconds, time must be equal to or greater than one minute
        :param time: str
        :returns: float
        """
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
    def convert_minutes(seconds):
        """
        Converts the seconds to minutes, time must be greater then 59 seconds
        :param seconds: float
        :returns: str
        """
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
        """

        # If time is less than a minute
        if isinstance(time, float):
            return round(time + 2, 2)

        # If time is over 59 seconds
        elif isinstance(time, str):
            time = time.replace(".", ":")
            minute, seconds, miliseconds = time.split(":")

            if seconds[0] == "0":
                seconds = seconds[1]

            seconds = int(seconds)
            seconds += 2
            seconds = "0" + str(seconds)

            return minute + ":" + str(seconds) + "." + miliseconds

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


if __name__ == "__main__":
    print (" ".join(CubeUtils.generate_scramble()))

