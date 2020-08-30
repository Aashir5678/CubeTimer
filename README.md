# CubeTimer
A Rubik's cube timer made with Tkinter in Python

## Installation
```bash

```
## Usage
CubeTimer is used to record and store Rubik's Cube times in a database, for any NXN puzzle type, to setup a Cube Timer app, use the code below:
```python
from CubeTimer import CubeTimer
import tkinter as tk

root = tk.Tk()
cube_timer = CubeTimer(root)
root.mainloop()
```

## Settings
If you need to change anything about your timer, then you can change it in the settings window, to enter settings, click the gear in the top left


### Time Table
You can access your times in a table by pressing t, or by going to settings and pressing the **View times in table** button, here you can view all of your recorded times in a table which displays the times scramble, date and whether or not it is a DNF.

![Time Table](/Screenshots/TimeTable.png)

## Export times
Lets say you want to write your times in to a text file, how can you do that ? Well, you can export your times in to another file by pressing e or be pressing the **Export times** button in settings,
once you do, select a **text file** to export your times to

![Export times](/Screenshots/ExportTimesCropped.png)
## Import times
But what if you want to import times from a text file in to your CubeTimer ? You can press i or you can go to settings and press **Import times**, then, select a text file to import times from, if this file was written manually, and not exported, then write the text file in the format of the image above. An example of a time is seen here

**10.45, F L B F2 R D' L B F' R2 D L2 R B L D2 U2 B' F U2 L2 B F', 2020-08-29-7:43 PM**

## Inspection
If you want to have WCA inspection enabled or disabled, go to settings, and you'll see a checkbutton, if its checked, then inspection is on, if not then it isn't. WCA inspection lasts 15 seconds, so you have 15 seconds to look at your scrambled cube. If you exceed 15 seconds, then you can get a plus 2 or even a DNF, which are both penalties

## Penalties
But, what exactly are penalties ? Penalties happen if your solve wasn't done properly, like for example, if you are one turn away from solving the cube, but you stopped the timer before you solved it, then its a plus 2, but if it was more than 1 turn away from being solved and you stopped the timer, it's a DNF. Plus 2 is self explanitory, it adds two seconds to your time, DNF stands for Did Not Finish, it's the worst possible time you can get, if you have 2 DNF's in one solve, the average is DNF. You can DNF / plus 2 a time, by clicking on it in the listbox with all your times, then press the button with the desired penalty.

### Keybinds
- e - Export times
- i - Import times
- Space - Start / Stop Timer
- t - Display times in a Time Table
- F11 - Toggle fullscreen
- Escape - Exits fullscreen



## License
[MIT](https://choosealicense.com/licenses/mit/)
