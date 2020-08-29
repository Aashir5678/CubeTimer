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

### Keybinds
- e - Export times
- i - Import times
- Space - Start / Stop Timer
- t - Display times in a Time Table
- F11 - Toggle fullscreen
- Escape - Exits fullscreen



## License
[MIT](https://choosealicense.com/licenses/mit/)
