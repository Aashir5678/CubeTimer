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
once you do, select a *text file* to export your times to

![Export times](/Screenshots/ExportTimes.png)
## Import times

### Keybinds
- e - Export times
- i - Import times
- Space - Start / Stop Timer
- t - Display times in a Time Table
- F11 - Toggle fullscreen
- Escape - Exits fullscreen



## License
[MIT](https://choosealicense.com/licenses/mit/)