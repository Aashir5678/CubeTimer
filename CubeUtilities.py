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
            # Generate a random letter notation
            letter = random.choice(cls.LETTERS)
            if letter_index != 0:
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
            scramble.append(letter)

        # scramble[-1] = scramble[-1].replace("\n", "")

        return scramble

    @classmethod
    def get_best_time(cls, times) -> int:
        """
        Returns the best time
        :param list times: a list of times
        :returns: int
        """
        return min(times)

    @classmethod
    def get_worst_time(cls, times) -> int:
        """
        Returns the worst time
        :param list times: a list of times
        :returns: int
        """
        return max(times)

    @classmethod
    def validate(cls, scramble) -> bool:
        """
        Returns True if scramble is valid, else, returns False
        :param list scramble:
        :return: bool
        """
        prev_move = scramble[0]
        for move in scramble[1: -1]:
            if move == prev_move:
                return False

            prev_move = move

        return True

    @staticmethod
    def get_average(times, ao=-1) -> float:
        """
        Returns average of times depending on ao parameter
        :param list times: A list of times
        :param int ao: defaults to -1 (the whole list)
        :return: float
        """
        if len(times) == 0:
            return 0.0

        elif len(times) == 1:
            return times[0]

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
            times_.remove(max(times_))
            times_.remove(min(times_))

        for time in range(len(times_)):
            times_[time] = float(times_[time])

        try:
            return round(float(sum(times_)) / float(len(times_)), 2)

        except ZeroDivisionError:
            return 0.0


class Time:
    def __init__(self, time, scramble, date):
        """
        :param time: float
        :param scramble: str
        :param date: datetime.datetime
        """
        if not isinstance(date, datetime.datetime):
            raise TypeError("date parameter must be of type datetime.datetime")

        self.time = time
        self.scramble = scramble
        self.date = datetime.datetime.strftime(date, "%Y-%m-%d-%I:%M %p")

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

    for i in range(100):
        scramble = CubeUtils.generate_scramble()
        valid = CubeUtils.validate(scramble)

        if valid:
            print ("Valid")
            print (scramble)

        else:
            print ("Invalid")
            print (scramble)

    scramble = "B2 R' R' " + " ".join(CubeUtils.generate_scramble(10))
    print (CubeUtils.validate(scramble.split(" ")))

