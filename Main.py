# Imports
import sqlite3
import datetime
import time as t
import tkinter as tk
import tkinter.font as font
from pyperclip import copy
from pygame import mixer
from tkinter import messagebox
from _tkinter import TclError
from CubeUtilities import CubeUtils, Time, TimeTable
from PIL import ImageTk, Image
from os.path import exists
from tkinter.filedialog import askopenfilename


class CubeTimer:
    """Makes a cube timer application"""
    def __init__(self, parent):
        """
        :param parent: tk.Tk
        """
        # Screen setup / Initialization variables
        self.parent = parent
        self.parent.geometry("1500x1000")
        self.parent.title("Cube Timer")
        self.ICON_IMG = "Assets\\cube.ico" # Icon made by Freepik from www.flaticon.com
        self.parent.iconbitmap(self.ICON_IMG)
        self.parent.config(background="light green")
        self.fullscreen = False
        self.timer_is_running = False
        self.space_held = False
        self.display_time = False
        self.open_display_times = False
        self.DNF = False
        self.plus_2 = False
        self.scramble = None
        self.Settings = None
        self.times = []
        self.scramble_len = 25
        self.INSPECTION_COUNT = 16
        self.DATE_FORMAT = "%Y-%m-%d-%I:%M %p"
        self.ON_CLOSE = "WM_DELETE_WINDOW"
        self.best_time = 0
        self.worst_time = 0
        self.start = 0
        self.end = 0
        self.inspection_difference = -1
        self.Inspectionvar = tk.IntVar()
        self.Displaytimevar = tk.IntVar()

        # Create connection to database and create table
        self.conn = sqlite3.connect("Timer\\solves.db")
        self.c = self.conn.cursor()

        try:
            self.c.execute("""CREATE TABLE times (
                            time float,
                            scramble text,
                            date text,
                            DNF integer
                            )""")

        except sqlite3.OperationalError:
            pass

        # Initialize mixer
        mixer.init()
        mixer.music.load("Assets/beep.wav")

        self.c.execute("DELETE FROM times")

        # Get times
        self.c.execute("SELECT time, scramble, date, DNF FROM times")

        for times in self.c.fetchall():
            time, scramble, date, DNF = times
            date = datetime.datetime.strptime(date, self.DATE_FORMAT)
            if DNF:
                self.times.append(Time(time, scramble, date, DNF=True))

            else:
                self.times.append(Time(time, scramble, date))

        frame = tk.Frame(self.parent)

        # Get scramble length, inspection and display time values

        conn = sqlite3.connect("Timer\\settings.db")
        cursor = conn.cursor()
        try:
            settings = self.get_settings(cursor)
            if settings:
                self.Inspectionvar.set(settings[0][0])
                self.Displaytimevar.set(settings[0][1])
                self.display_time = (True if self.Displaytimevar.get() else False)
                self.scramble_len = settings[0][2]

        except sqlite3.OperationalError:
            pass

        finally:
            conn.close()

        # Setup Listbox
        self.TimesScrollbar = tk.Scrollbar(self.parent)
        if len(self.times) == 0:
            self.TimesListbox = tk.Listbox(self.parent, height=10)

        else:
            self.TimesListbox = tk.Listbox(self.parent, height=len(self.times))
            self.insert_times()

        self.TimesListbox.config(width=10)

        # Get ao5, ao12, ao100 and mean

        times = list(self.TimesListbox.get(0, tk.END))
        self.mean = "N/A"
        self.ao5 = "N/A"
        self.ao12 = "N/A"
        self.ao100 = "N/A"
        self.best_time = "N/A"
        self.worst_time = "N/A"

        try:
            times_ = []
            for time in self.times:
                if not time.DNF:
                    times_.append(time.time)

                else:
                    times_.append("DNF")
            self.best_time = CubeUtils.get_best_time(times_)

        except ValueError:
            pass

        try:
            times_ = []
            for time in self.times:
                if not time.DNF:
                    times_.append(time.time)

                else:
                    times_.append("DNF")
            self.worst_time = CubeUtils.get_worst_time(times_)

        except ValueError:
            pass

        if len(times) > 5 and len(times) >= 12 and len(times) >= 100:
            self.ao5 = CubeUtils.get_average(times, ao=5)
            self.ao12 = CubeUtils.get_average(times, ao=12)
            self.ao100 = CubeUtils.get_average(times, ao=100)
            self.mean = CubeUtils.get_average(times)

        elif len(times) >= 100:
            self.ao5 = CubeUtils.get_average(times, ao=5)
            self.ao12 = CubeUtils.get_average(times, ao=12)
            self.mean = CubeUtils.get_average(times)

        elif len(times) >= 5:
            self.ao5 = CubeUtils.get_average(times, ao=5)
            self.mean = CubeUtils.get_average(times)

        else:
            self.mean = CubeUtils.get_average(times)

        # Fonts

        self.timefont = font.Font(size=50)
        self.scramblefont = font.Font(size=40, weight="bold")
        self.averagefont = font.Font(size=15, weight="bold")

        # Images
        gear_image = Image.open("Assets\gear.png") # Icon made by Pixel perfect from www.flaticon.com
        gear_image = ImageTk.PhotoImage(gear_image)

        # Tkinter widgets
        self.InspectionLabel = tk.Label(self.parent, text=self.INSPECTION_COUNT, font=self.timefont, bg="red")

        self.TimeLabel = tk.Label(
            self.parent, text="0.00", bg="light green", font=self.timefont
        )
        scramble = self.get_scramble()
        self.ScrambleText = tk.Text(
            frame, height=1, width=200, font=self.scramblefont, bg="brown",
        )

        self.SettingsButton = tk.Button(self.parent, image=gear_image, bg="light green", relief=tk.FLAT,
                                        command=lambda: self.open_settings(), height=60, width=60)

        self.SettingsButton.image = gear_image
        self.AveragesLabel = tk.Label(self.parent, font=self.averagefont)

        self.update_stats(times)
        self.ScrambleText.insert("0.0", scramble)
        self.ScrambleText.config(state=tk.DISABLED)

        # Bindings

        self.parent.bind("t", lambda event: self.display_times())
        self.parent.bind("e", lambda event: self.export_times())
        self.parent.bind("i", lambda event: self.import_times())
        self.TimesListbox.bind(
            "<Double-Button-1>", lambda item: self.time_options()
        )

        self.TimesListbox.bind("<Delete>", lambda key: self.delete_time(self.TimesListbox.curselection()[0]
        )
        )

        self.SettingsButton.bind("<Enter>", lambda event: self.enlarge_settings_button())
        self.SettingsButton.bind("<Leave>", lambda event: self.shrink_settings_button())
        try:
            self.parent.protocol(self.ON_CLOSE, lambda: self.quit())

        except TclError:
            pass

        self.parent.bind("<F11>", lambda event: self.toggle_fullscreen())
        self.parent.bind("<Escape>", lambda event: self.exit_fullscreen())

        self.parent.bind(
            "<space>", lambda event: self.space_hold(),
        )

        # Widget placements

        frame.grid(row=0, column=0, sticky=tk.N)
        self.TimeLabel.grid(column=0, row=0)
        self.AveragesLabel.grid(
            row=1, column=0
        )
        self.ScrambleText.grid(row=0, column=0, sticky=tk.N, ipadx=5, ipady=5)
        self.SettingsButton.place(y=85)

        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.TimesListbox.grid(row=0, column=1, sticky=tk.N + tk.S)
        if len(self.times) >= 58:
            self.TimesScrollbar.grid(row=0, column=2, sticky=tk.N + tk.S)

        else:
            self.TimesListbox.grid(row=0, column=1, sticky=tk.N + tk.E)
        self.parent.columnconfigure(25)
        self.parent.rowconfigure(25)

    def save_time(self, time):
        """
        Saves the time to the database
        :param time: CubeUtilities.Time
        """
        self.times.append(time)
        with self.conn:
            self.c.execute("INSERT INTO times VALUES (?, ?, ?, ?)", (time.time, time.scramble, time.date, int(time.DNF)))

    def delete_time(self, oid, parent=None, confirm=True):
        """
        Deletes the time from the list and the database, if confirm then ask to delete time before deleting it,
        if parent is not None then it destroys the parent after deleting the time
        :param oid: int
        :param parent: tkinter.Tk()
        :param confirm: bool
        """
        if confirm:
            delete_time = tk.messagebox.askyesno("Delete time ?", "Are you sure you want to delete this time ?")

        else:
            delete_time = True

        if delete_time:
            oid += 1
            time = self.get_time(oid)

            if isinstance(time[0][0], str):
                time[0][0] = Time.convert_to_seconds(time)

            if self.TimesListbox.get(oid-1) == "DNF":
                time = Time(time[0][0], time[0][1], datetime.datetime.strptime(time[0][2], self.DATE_FORMAT), DNF=True)

            else:
                time = Time(time[0][0], time[0][1], datetime.datetime.strptime(time[0][2], self.DATE_FORMAT))

            for time_ in self.times:
                if time_.time == time.time and time_.scramble == time.scramble and time_.date == time.date and time_.DNF == time.DNF:
                    self.times.remove(time_)
                    break

            else:
                tk.messagebox.showerror("Non-existant time", f"The time '{time.time}' does not exist")
                return

            with self.conn:
                self.c.execute("SELECT oid FROM times")
                self.c.execute("DELETE FROM times WHERE oid = :oid",
                               {"oid": oid})
                self.c.execute("UPDATE times SET oid=:oid", {"oid": oid})

            self.insert_times()

            self.update_stats(list(self.TimesListbox.get(0, tk.END)))
            if parent is not None:
                parent.destroy()

    def get_time(self, oid) -> list:
        """
        Returns the times time, scramble and date
        :param oid: int
        :return: list[tuple]
        """
        self.c.execute("SELECT * FROM times WHERE oid=:oid", {"oid": oid})
        return self.c.fetchall()

    def get_settings(self, cursor) -> list:
        """
        Returns the current user settings
        :param cursor: conn.cursor()
        :return: list
        """
        cursor.execute("SELECT * FROM settings")
        return cursor.fetchmany(3)

    def get_scramble(self) -> str:
        """
        Generates a scramble of length self.length
        :return: str
        """
        self.scramble = " ".join(CubeUtils.generate_scramble(self.scramble_len))

        return self.scramble

    def start_timer(self, recursive=False):
        """Starts the timer"""
        if (not self.timer_is_running and not self.Inspectionvar.get()) or recursive:
            # Forget InspectionLabel and grid TimeLabel
            self.InspectionLabel.grid_forget()
            self.TimeLabel.config(text="0.00")
            self.TimeLabel.grid(row=0, column=0)

            # Unbind keys
            self.parent.unbind("<KeyRelease-space>")
            self.parent.unbind("<space>")

            # Change bg
            self.parent.config(bg="light green")
            self.TimeLabel.config(bg="light green")
            self.AveragesLabel.config(bg="light green")
            self.SettingsButton.config(bg="light green")

            # Start Timer
            self.space_held = False
            self.timer_is_running = True
            if self.display_time:
                self.TimeLabel.config(text="0.00")

            else:
                self.TimeLabel.config(text="...")
            self.start = t.time()
            self.update_timer()

            self.parent.bind(
                "<space>", lambda event: self.stop_timer(),
            )

        # Inspection
        elif not self.timer_is_running and self.Inspectionvar.get():
            if len(self.TimeLabel.grid_info()) != 0:
                self.TimeLabel.grid_forget()

            if self.inspection_difference != -1:
                self.inspection_difference += 1

                difference = self.INSPECTION_COUNT - self.inspection_difference

            else:
                self.inspection_difference = 1
                difference = self.INSPECTION_COUNT - self.inspection_difference

            if difference < 1:
                if difference > -3:
                    difference = "+2"

                else:
                    difference = "DNF"
                    self.DNF = True

            elif difference == 8 or difference == 4:
                mixer.music.play()

            self.InspectionLabel.config(text=difference)
            if len(self.InspectionLabel.grid_info()) == 0:
                self.InspectionLabel.grid(row=0, column=0)

            # Bindings
            self.parent.bind("<space>", lambda event: self.space_hold(recursive=True))
            self.InspectionLabel.after(1000, lambda: self.start_timer())

    def space_hold(self, recursive=False):
        """
        Bound to space down
        :param recursive: bool
        """
        # Unbind space and space release
        self.parent.unbind("<space>")
        self.parent.unbind("<KeyRelease-space>")

        if self.InspectionLabel["text"] == "+2":
            self.plus_2 = True

        # Reset inspection
        self.inspection_difference = -1

        # Change bg
        self.parent.config(bg="red")
        self.TimeLabel.config(bg="red")
        self.AveragesLabel.config(bg="red")
        self.SettingsButton.config(bg="red")

        # Bindings
        if not recursive:
            self.parent.bind("<KeyRelease-space>", lambda event: self.start_timer())

        else:
            self.parent.bind("<KeyRelease-space>", lambda event: self.start_timer(recursive=True))

    def stop_timer(self):
        """Stop the timer"""
        if self.timer_is_running:
            # Unbind and stop timer
            self.parent.unbind("<space>")
            self.parent.unbind("<KeyRelease-space>")
            self.timer_is_running = False
            self.end = t.time()

            if not self.display_time:
                self.display_time = True
                self.timer_is_running = True
                self.update_timer(recursive=False)
                self.display_time = False
                self.timer_is_running = False

            # Change bg
            self.TimeLabel.config(bg="red")
            self.AveragesLabel.config(bg="red")
            self.parent.config(bg="red")
            self.SettingsButton.config(bg="red")

            self.TimeLabel.after(100)

            self.TimeLabel.config(bg="light green")
            self.AveragesLabel.config(bg="light green")
            self.parent.config(bg="light green")
            self.SettingsButton.config(bg="light green")

            # Generate and displaying the scramble
            self.ScrambleText.config(state=tk.NORMAL)
            self.ScrambleText.delete("0.0", tk.END)
            scramble_text = self.get_scramble()

            self.ScrambleText.insert("0.0", scramble_text)
            self.ScrambleText.config(state=tk.DISABLED)
            self.ScrambleText.config(state=tk.DISABLED)

            # Add time to listbox
            self.TimesListbox.config(height=len(self.times) + 1)
            if not self.plus_2 and not self.DNF:
                self.TimesListbox.insert(tk.END, self.TimeLabel["text"])

            elif self.plus_2:
                self.TimesListbox.insert(tk.END, float(self.TimeLabel["text"]) + 2)

            else:
                self.TimesListbox.insert(tk.END, "DNF")

            if len(self.times) >= 58:
                self.TimesScrollbar.grid(row=0, column=2, sticky=tk.N + tk.S)

            else:
                self.TimesListbox.grid(row=0, column=1, sticky=tk.N + tk.E)

            times = list(self.TimesListbox.get(0, tk.END))

            # Add time to self.times and database
            now = datetime.datetime.now()
            time_date = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute)
            time = self.TimeLabel["text"]

            # If time is greater than 59 seconds
            if Time.convert_to_seconds(time) != 0.0:
                time = Time.convert_to_seconds(time)

            if not self.plus_2 and not self.DNF:
                time = Time(float(time), self.scramble, time_date)

            elif self.plus_2:
                time = Time(float(time + 2), self.scramble, time_date)

            else:
                time = Time(float(time), self.scramble, time_date, DNF=True)

            self.save_time(time)
            self.plus_2 = False
            self.DNF = False

            # Update stats
            self.update_stats(times)

            # Rebind start timer and space releases
            self.parent.after(300)
            self.parent.bind(
                "<space>", lambda event: self.space_hold(),
            )

    def time_options(self):
        """Opens the time options in a new tkinter.Tk() window"""
        self.TimeOptions = tk.Tk()
        self.TimeOptions.title("Time Options")
        self.TimeOptions.iconbitmap(self.ICON_IMG) # Icon made by Freepik from www.flaticon.com

        try:
            time = self.TimesListbox.get(self.TimesListbox.curselection()[0])
            oid = self.TimesListbox.get(0, tk.END).index(time)
            oid += 1

        except IndexError:
            return

        def on_close():
            """Called when TimeOptions is closed"""
            self.TimesListbox.config(state=tk.NORMAL)
            self.TimeOptions.destroy()
            self.parent.focus()

        self.unfocus_times()

        if ":" in str(time):
            time_info = list(self.get_time(oid))[0]

            if not time_info:
                tk.messagebox.showerror("Non-existant time", f"The time '{time}' does not exist.'")
                return

            time = time_info[0]
            scramble = time_info[1]
            date = time_info[2]
            date = datetime.datetime.strptime(date, self.DATE_FORMAT)

            time = Time(float(time), scramble, date)

        else:
            time_info = list(self.get_time(oid))[0]

            if not time_info:
                tk.messagebox.showerror("Non-existant time", f"The time '{time}' does not exist.'")
                return

            time = time_info[0]
            scramble = time_info[1]
            date = time_info[2]
            date = datetime.datetime.strptime(date, self.DATE_FORMAT)

            time = Time(float(time), scramble, date)

        timefont = font.Font(size=15)

        if time.time > 59:
            TimeLabel = tk.Label(self.TimeOptions, text=Time.convert_to_minutes(time.time), font=timefont)

        elif not time.DNF:
            TimeLabel = tk.Label(self.TimeOptions, text=time.time, font=timefont)

        else:
            TimeLabel = tk.Label(self.TimeOptions, text="DNF", font=timefont)

        DateLabel = tk.Label(self.TimeOptions, text=time.date)
        ScrambleLabel = tk.Label(self.TimeOptions, text=time.scramble)
        if time.DNF:
            DeleteTimeButton = tk.Button(self.TimeOptions, text="Delete",
                                         command=lambda: self.delete_time(self.TimesListbox.curselection()[0],
                                                                          parent=self.TimeOptions))

        else:
            DeleteTimeButton = tk.Button(self.TimeOptions, text="Delete",
                                         command=lambda: self.delete_time(self.TimesListbox.curselection()[0],
                                                                          parent=self.TimeOptions))

        DNFButton = tk.Button(self.TimeOptions, text="DNF")
        Plus2Button = tk.Button(self.TimeOptions, text="+2")

        # Bindings
        self.TimeOptions.bind("<Delete>", lambda event: self.delete_time(self.TimesListbox.curselection()[0],
                                                                         parent=self.TimeOptions))
        self.TimeOptions.protocol(self.ON_CLOSE, on_close)
        DNFButton.bind("<Button-1>", lambda event: self.DNF_time(oid, parent=self.TimeOptions))
        Plus2Button.bind("<Button-1>", lambda event: self.plus_2_time(oid, parent=self.TimeOptions))

        TimeLabel.grid(row=0, column=1)
        ScrambleLabel.grid(row=1, column=1)
        DateLabel.grid(row=2, column=1)
        DeleteTimeButton.grid(row=3, column=0)
        if not time.DNF:
            DNFButton.grid(row=3, column=1)
        Plus2Button.grid(row=3, column=2)

    def DNF_time(self, oid, parent=None):
        """
        DNF's the time with the oid provided, destroys parent if parent is not None
        :param oid: int
        :param parent: tkinter.Tk()
        """
        with self.conn:
            self.c.execute("UPDATE times SET DNF=1 WHERE oid=:oid", {"oid": oid})

        time_info = list(self.get_time(oid))[0]
        time = Time(time_info[0], time_info[1], datetime.datetime.strptime(time_info[2], self.DATE_FORMAT), DNF=True)
        self.times[oid-1] = time
        self.insert_times()

        if parent is not None:
            parent.destroy()

    def plus_2_time(self, oid, parent=None):
        """
        Add 2 seconds to the time with the oid provided
        :param oid: int
        :param parent: tkinter.Tk
        """
        time = list(self.get_time(oid))[0][0]
        time = round(float(time + 2), 2)
        self.c.execute("UPDATE times SET time=:time WHERE oid=:oid", {"time": time, "oid": oid})
        time_info = list(self.get_time(oid))[0]

        # Not DNF
        if not time_info[-1]:
            time = Time(time_info[0], time_info[1], datetime.datetime.strptime(time_info[2], self.DATE_FORMAT))

        # DNF
        else:
            time = Time(time_info[0], time_info[1], datetime.datetime.strptime(time_info[2], self.DATE_FORMAT), DNF=True)

        self.times[oid-1] = time
        self.insert_times()

        if parent is not None:
            parent.destroy()

    def open_settings(self):
        """Opens the settings in a new tkinter.Tk() window"""
        # Settings window setup
        if self.Settings is not None:
            self.Settings.destroy()

        self.Settings = tk.Tk()
        self.Settings.geometry("600x240")
        self.Settings.iconbitmap(self.ICON_IMG)
        self.Settings.resizable(False, False)
        self.Settings.title("Settings")

        # Connect to database

        conn = sqlite3.connect("Timer\\settings.db")
        cursor = conn.cursor()

        try:
            cursor.execute("""CREATE TABLE settings (
                                    inspection integer,
                                    display_time integer,
                                    scramble_len integer
                                    )""")

        except sqlite3.OperationalError:
            pass

        # Check if inspection is enabled and set scramble length

        if self.get_settings(cursor):
            self.Inspectionvar.set(self.get_settings(cursor)[0][0])
            self.Displaytimevar.set(self.get_settings(cursor)[0][1])
            self.scramble_len = int(self.get_settings(cursor)[0][2])

            self.display_time = (True if int(self.get_settings(cursor)[0][1]) else False)

        else:
            self.Inspectionvar.set(0)
            self.Displaytimevar.set(1)
            self.display_time = True
            with conn:
                cursor.execute("DELETE FROM settings")
                cursor.execute("INSERT INTO settings VALUES (:inspection, :display_time, :scramble_len)",
                               {"inspection": self.Inspectionvar.get(), "display_time": self.Displaytimevar.get(),
                                "scramble_len": self.scramble_len})

        # Setting widgets
        SettingFont = font.Font(size=40, weight="bold")
        SettingsLabel = tk.Label(self.Settings, text="Settings", font=SettingFont)
        self.DisplayTimeCheckbutton = tk.Checkbutton(self.Settings, text="Display time", variable=self.Displaytimevar,
                                                     offvalue=0,
                                                     onvalue=1)

        self.InspectionCheckbutton = tk.Checkbutton(self.Settings, text="Inspection", variable=self.Inspectionvar,
                                                    offvalue=0,
                                                    onvalue=1
                                                    )

        if self.Inspectionvar.get():
            self.InspectionCheckbutton.select()

        if self.display_time:
            self.DisplayTimeCheckbutton.select()

        ScrambleLabel = tk.Label(self.Settings, text="Scramble length:")
        ScrambleEntry = tk.Entry(self.Settings)

        ImportTimesButton = tk.Button(self.Settings, text="Import times")
        ExportTimesButton = tk.Button(self.Settings, text="Export times")
        ClearSolvesButton = tk.Button(self.Settings, text="Clear times", command=self.clear_times)
        CopyTimesButton = tk.Button(self.Settings, text="Copy times")
        DisplayTimesButton = tk.Button(self.Settings, text="View times in table", command=self.display_times)
        GenerateScrambleButton = tk.Button(self.Settings, text="Generate scramble", command=self.insert_scramble)
        ShowKeyBindsButton = tk.Button(self.Settings, text="Show Keybindings", command=CubeTimer.show_keybindings)

        ScrambleEntry.insert(0, self.scramble_len)

        # Bindings
        ScrambleEntry.bind("<Return>", lambda event: self.change_scramble_len(conn, cursor, ScrambleEntry))
        CopyTimesButton.bind("<Button-1>", lambda event: self.copy_times(CopyTimesButton))
        ImportTimesButton.bind("<Button-1>", lambda event: self.import_times())
        ExportTimesButton.bind("<Button-1>", lambda event: self.export_times())
        self.InspectionCheckbutton.bind("<Button-1>", lambda event: self.save_setting(conn, cursor))
        self.DisplayTimeCheckbutton.bind("<Button-1>", lambda event: self.save_setting(conn, cursor, setting="display time"))
        self.Settings.protocol(self.ON_CLOSE,
                               lambda: self.change_scramble_len(conn, cursor, ScrambleEntry, quit_window=True))

        # Widget placement
        SettingsLabel.pack()
        self.InspectionCheckbutton.pack()
        self.DisplayTimeCheckbutton.pack()
        ScrambleLabel.pack()
        ScrambleEntry.pack()
        ClearSolvesButton.place(x=260, y=200)
        CopyTimesButton.place(x=260, y=125)
        ShowKeyBindsButton.place(x=240, y=160)
        GenerateScrambleButton.place(x=100, y=200)
        DisplayTimesButton.place(x=400, y=200)
        ExportTimesButton.place(x=400, y=125)
        ImportTimesButton.place(x=100, y=125)

    def import_times(self, filename=None):
        """
        Imports the times in to the current session, the contents of the Text widget or the file
        must follow the format as followed, brackets aren't required and if times are stored in
        file, you must separate by a new line

        Text widget:
        (5.43), 32.43, 23.58, (45.76)

        File:
        (5.43)
        43.43
        (4.43)
        55.84

        :param filename: str
        """

        # Get the contents of Text widget / file

        imported_times = []
        if filename is None:
            filename = askopenfilename()
            if not filename.endswith(".txt"):
                tk.messagebox.showerror("Invalid extension", "File extension must be .txt")
                return

        if exists(filename):
            with open(filename, "r") as f:
                times = f.readlines()
                for time in times:
                    info = time.split(", ")
                    if len(info) == 3:
                        DNF = False
                        time_, scramble, date = info

                    elif len(info) == 4:
                        DNF = True
                        time_, scramble, date, _ = info

                    else:
                        return
                    time_ = time_.replace("(", "").replace(")", "")
                    date = date.replace("\n", "")
                    date = datetime.datetime.strptime(date, self.DATE_FORMAT)
                    if not DNF:
                        imported_times.append(Time(float(time_), scramble, date))

                    else:
                        imported_times.append(Time(float(time_), scramble, date, DNF=True))

                    if len(times) == len(imported_times):
                        break

                else:
                    return

        else:
            tk.messagebox.showerror("Invalid path", "This path does not exist.")
            return

        # Save times
        for time in imported_times:
            self.save_time(time)

        # Insert times in to TimesListbox
        self.insert_times()

    def export_times(self, filename=None):
        """
        Exports the times in the current session to a file, contents of file will be overwritten
        :param filename: str
        """
        if filename is None:
            filename = askopenfilename()

        if not filename.endswith(".txt"):
            tk.messagebox.showerror("Invalid extension", "File extension must be .txt")
            return

        if not exists(filename):
            file = open(filename, "x")
            file.close()

        to_write = []
        for time in self.times:
            if time.DNF:
                line = f"{time.time}, {time.scramble}, {time.date}, DNF"
                to_write.append(line)

            else:
                line = f"{time.time}, {time.scramble}, {time.date}"
                to_write.append(line)

        to_write = "\n".join(to_write)
        with open(filename, "w") as f:
            f.write(to_write)

    def reset_window(self, time_table):
        """
        Resets the window, but preserves times and setting options
        :param time_table: CubeUtilities.TimeTable
        """
        for widget in time_table.winfo_children():
            widget.destroy()

        try:
            self.Settings.destroy()

        except (AttributeError, TclError):
            pass

        time_table.destroy()
        self.__init__(self.parent)

    def display_times(self):
        """
        Displays all times in the current session, along with its scramble, date and whether or not
        the time is a DNF
        """
        self.parent.title("Time Table")
        self.parent.unbind("<space>")
        self.parent.unbind("<F11>")
        self.parent.unbind("<Escape>")

        try:
            self.Settings.destroy()

        except (AttributeError, TclError):
            pass

        try:
            self.TimeOptions.destroy()

        except (AttributeError, TclError):
            pass

        for widget in self.parent.winfo_children():
            widget.destroy()

        time_table = TimeTable(self.parent, self.times)
        time_table.grid(row=0, column=0, stick="NESW")

        self.parent.bind("t", lambda event: self.reset_window(time_table))

    def change_scramble_len(self, conn, cursor, entry, quit_window=False):
        """
        Gets the int from the entry provided and sets it to the new scramble length
        :param conn: sqlite3.connect(db)
        :param cursor: conn.cursor
        :param entry: tkinter.Entry
        :param quit_window: bool
        """
        try:
            if self.scramble_len == int(entry.get()):
                if quit_window:
                    try:
                        self.Settings.destroy()
                        self.Settings = None

                    except TclError:
                        pass

                    finally:
                        return

            self.scramble_len = int(entry.get())

        except ValueError:
            return

        else:
            self.ScrambleText.config(state=tk.NORMAL)
            self.ScrambleText.delete("0.0", tk.END)
            self.parent.update()
            scramble = self.get_scramble()
            self.ScrambleText.insert("0.0", scramble)
            self.parent.update()
            self.ScrambleText.config(state=tk.DISABLED)

        self.save_setting(conn, cursor, setting=entry)
        if quit_window:
            conn.close()
            self.Settings.destroy()

    def copy_times(self, button):
        """
        Copies all the times to clipboard, each time is seperated by a comma
        :param button: tkinter.Button
        """
        to_copy = ""
        max_found = False
        min_found = False
        times = list(time.time if not time.DNF else "DNF" for time in self.times)

        for time in self.times:
            # Check if the the time is the last element of self.times
            if self.times[-1] != time:
                # Check if the current time is the best in the list
                if time.time == CubeUtils.get_best_time(times) and not max_found:
                    if not time.DNF:
                        to_copy += f"({time.time}), "

                    else:
                        to_copy += "(DNF), "

                # Check if the current time is the worst time in the list
                elif time.time == CubeUtils.get_worst_time(times) and not min_found:
                    if not time.DNF:
                        to_copy += f"({time.time}), "

                    else:
                        to_copy += "(DNF), "

                else:
                    if not time.DNF:
                        to_copy += f"{time.time}, "

                    else:
                        to_copy += "DNF, "

            else:
                # Check if the current time is the best in the list
                if time.time == CubeUtils.get_best_time(times) and not max_found:
                    if not time.DNF:
                        to_copy += f"({time.time})"

                    else:
                        to_copy += "(DNF)"

                # Check if the current time is the worst time in the list
                elif time.time == CubeUtils.get_worst_time(times) and not min_found:
                    if not time.DNF:
                        to_copy += f"({time.time})"

                    else:
                        to_copy += "(DNF)"

                else:
                    if not time.DNF:
                        to_copy += f"{time.time}"

                    else:
                        to_copy += "(DNF)"

        copy(to_copy)
        button.config(text="Copied")

        button.after(3000, lambda: button.config(text="Copy times"))

    def clear_times(self):
        """Clears all times"""
        delete_times = tk.messagebox.askyesno("Delete all times", "Are you sure you want to clear all your times ?")
        if delete_times:
            self.TimesListbox.delete(0, tk.END)
            self.TimesListbox.config(height=5)
            self.times.clear()
            with self.conn:
                self.c.execute("DELETE FROM times")

            self.update_stats(self.TimesListbox.get(0, tk.END))

            self.TimeLabel.config(text="0.00")

    def insert_scramble(self):
        """Generates a scramble and inserts it to ScrambleText"""
        self.ScrambleText.config(state=tk.NORMAL)
        self.ScrambleText.delete("0.0", tk.END)
        scramble = self.get_scramble()
        self.ScrambleText.insert("0.0", scramble)
        self.ScrambleText.config(state=tk.DISABLED)
        self.parent.update()

    def enlarge_settings_button(self):
        """Enlarges the settings button, bound to mouse hover"""
        image = Image.open("Assets\\gear.png")
        image = image.resize((66, 66), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        self.SettingsButton.config(image=image)
        self.SettingsButton.image = image

    def shrink_settings_button(self):
        """Shrinks the settings button to its default size"""
        image = Image.open("Assets\\gear.png")
        image = image.resize((60, 60), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        self.SettingsButton.config(image=image)
        self.SettingsButton.image = image

    def save_setting(self, conn, cursor, setting="inspection"):
        """
        Saves the setting, 'setting', by default, saving value of Inspectionvar, if the setting is of instance
        tkinter.Entry, then save the scramble length, which is fetched by the entry provided
        :param conn: sqlite3.connect(db)
        :param cursor: conn.cursor()
        :param setting: str or tkinter.Entry
        """
        if setting == "inspection":
            if self.Inspectionvar.get():
                self.Inspectionvar.set(0)

            else:
                self.Inspectionvar.set(1)

            inspection = self.Inspectionvar.get()
            with conn:
                cursor.execute("UPDATE settings SET inspection = :inspection WHERE display_time = :display_time", {"inspection": inspection, "display_time": int(self.display_time)})

        elif setting == "display time":
            if self.Displaytimevar.get():
                self.Displaytimevar.set(0)
                self.display_time = False

            else:
                self.Displaytimevar.set(1)
                self.display_time = True

            display_time = self.Displaytimevar.get()

            with conn:
                cursor.execute("UPDATE settings SET display_time= :display_time WHERE scramble_len = :length", {"display_time": display_time, "length": self.scramble_len})

        elif isinstance(setting, tk.Entry):
            with conn:
                cursor.execute("UPDATE settings SET scramble_len=:length WHERE inspection=:inspection", {"length": self.scramble_len, "inspection": self.Inspectionvar.get()})

    def update_timer(self, recursive=True):
        """
        Updates the timer, if recursive, updates the timer every 100 miliseconds
        :param recursive: bool
        """
        self.mean = "N/A"
        self.ao5 = "N/A"
        self.ao12 = "N/A"
        self.ao100 = "N/A"
        if self.timer_is_running:
            end = t.time()
            diff = end - self.start

            # Checks if diff is greater than or equal to a minute
            if round(diff) >= 60:
                diff = Time.convert_to_minutes(diff)

                if len(diff.split(".")[-1]) == 1:
                    diff += "0"

            elif round(diff) >= 10:
                diff = str(diff)
                diff = diff[0:4] + diff[4]

            # Checks if diff is smaller then ten
            else:
                diff = str(diff)
                try:
                    diff = diff[0:3] + diff[3]

                except IndexError:
                    diff = diff[0:2] + diff[2]

            if self.display_time:
                self.TimeLabel.config(text=diff)

        self.parent.update()

        # Calls it self every 100 miliseconds
        if recursive:
            self.TimeLabel.after(100, lambda: self.update_timer())

    def update_stats(self, times):
        """
        Calculate and display ao5, ao12, ao100, mean, best and worst time
        :param times: string list
        """
        # Convert to float array
        for time in range(len(times)):
            try:
                times[time] = float(times[time])

            # DNF / time over 60 seconds
            except ValueError:
                if times[time] != "DNF":
                    times[time] = Time.convert_to_seconds(times[time])

        # Get best and worst times

        try:
            self.best_time = CubeUtils.get_best_time(times)

        except ValueError:
            self.best_time = "N/A"

        try:
            self.worst_time = CubeUtils.get_worst_time(times)

        except ValueError:
            self.worst_time = "N/A"

        # Get mean, ao5, ao12 and ao100
        if len(self.times) >= 100:
            self.mean = CubeUtils.get_average(times)
            self.ao5 = CubeUtils.get_average(times, ao=5)
            self.ao12 = CubeUtils.get_average(times, ao=12)
            self.ao100 = CubeUtils.get_average(times, ao=100)

        elif len(self.times) > 5 and len(self.times) >= 12:
            self.mean = CubeUtils.get_average(times)
            self.ao5 = CubeUtils.get_average(times, ao=5)
            self.ao12 = CubeUtils.get_average(times, ao=12)

        elif len(times) >= 5:
            self.mean = CubeUtils.get_average(times)
            self.ao5 = CubeUtils.get_average(times, ao=5)

        else:
            self.mean = CubeUtils.get_average(times)

        if isinstance(self.mean, float) or isinstance(self.mean, int):
            if self.mean > 59:
                self.mean = Time.convert_to_minutes(self.mean)

        if isinstance(self.ao5, float) or isinstance(self.ao5, int):
            if self.ao5 > 59:
                self.ao5 = Time.convert_to_minutes(self.ao5)

        if isinstance(self.ao12, float) or isinstance(self.ao12, int):
            if self.ao12 > 59:
                self.ao12 = Time.convert_to_minutes(self.ao12)

        if isinstance(self.ao100, float) or isinstance(self.ao100, int):
            if self.ao100 > 59:
                self.ao100 = Time.convert_to_minutes(self.ao100)

        if isinstance(self.best_time, float) or isinstance(self.best_time, int):
            if self.best_time > 59:
                self.best_time = Time.convert_to_minutes(self.best_time)

        if isinstance(self.worst_time, float) or isinstance(self.worst_time, int):
            if self.worst_time > 59:
                self.worst_time = Time.convert_to_minutes(self.worst_time)

        # Display stats
        self.AveragesLabel.config(
            text="mean: "
                 + str(self.mean)
                 + " ao5: "
                 + str(self.ao5)
                 + " ao12: "
                 + str(self.ao12)
                 + " ao100: "
                 + str(self.ao100) + " best: " + str(self.best_time) + " worst: " + str(self.worst_time)
                 + " solves: " + str(len(self.times)),
            bg="light green",
            font=self.averagefont,
        )

    def insert_times(self):
        """Inserts every time in self.times in to self.TimesListbox"""
        self.TimesListbox.config(state=tk.NORMAL)
        self.TimesListbox.delete(0, tk.END)

        if len(self.times) >= 5:
            self.TimesListbox.config(height=len(self.times), yscrollcommand=self.TimesScrollbar.set)
            self.TimesScrollbar.config(command=self.TimesListbox.yview())

        else:
            self.TimesListbox.config(height=5)

        for time in self.times:
            if not time.DNF:
                if time.time > 59:
                    self.TimesListbox.insert(tk.END, Time.convert_to_minutes(time.time))

                else:
                    self.TimesListbox.insert(tk.END, time.time)

            else:
                self.TimesListbox.insert(tk.END, "DNF")

        self.TimesListbox.update()

    def unfocus_times(self):
        """Un-highlights any item from TimesListbox"""
        self.TimesListbox.config(state=tk.DISABLED)
        self.parent.focus()

    def toggle_fullscreen(self):
        """Puts the window in fullscreen"""
        self.fullscreen = not self.fullscreen
        self.parent.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self):
        """Exits fullscreen"""
        self.fullscreen = False
        self.parent.attributes("-fullscreen", self.fullscreen)

    @staticmethod
    def show_keybindings():
        """Shows all the keybindings for the Cube Timer"""
        tk.messagebox.showinfo(
            "Key bindings",
            "Key Bindings\ni - Import Times\ne - Export Times\nt - Enter / Exit Time Table\nDel - Deletes highlighted time in the list of times\nF11 - Toggle fullscreen\nEscape - Exit fullscreen"
        )

    def quit(self):
        """Quits the window and any other opened windows"""
        try:
            self.Settings.destroy()

        except (TclError, AttributeError):
            pass

        try:
            self.TimeOptions.destroy()

        except (TclError, AttributeError):
            pass

        self.conn.close()
        self.parent.quit()


def main():
    root = tk.Tk()
    app = CubeTimer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
