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
### Time Table
You can acess your times in a table by pressing t, or by going to settings and pressing the **View times in table** button, here you can view all of your recorded times in a table which displays the times scramble, date and whether or not it is a DNF.

![Time Table](/Assets/TimeTable.png)

### Keybinds
- e - Export times
- i - Import times
- Space - Start / Stop Timer
- t - Display times in a Time Table
- F11 - Toggle fullscreen
- Escape - Exits fullscreen



## License
[MIT](https://choosealicense.com/licenses/mit/)
