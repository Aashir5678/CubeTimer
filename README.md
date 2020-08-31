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
If you need to change anything about your timer, then you can change it in the settings window, to enter settings, click the gear in the top left.


### Time Table
You can access your times in a table by pressing t, or by going to settings and pressing the **View times in table** button, here you can view all of your recorded times in a table which displays the times scramble, date and whether or not it is a DNF.

![Time Table](/Screenshots/TimeTable.png)

### Export times
Lets say you want to write your times in to a text file, how can you do that ? Well, you can export your times in to another file by pressing e or be pressing the **Export times** button in settings,
once you do, select a **text file** to export your times to.

![Export times](/Screenshots/ExportTimesCropped.png)
### Import times
But what if you want to import times from a text file in to your CubeTimer ? You can press i or you can go to settings and press **Import times**, then, select a text file to import times from, if this file was written manually, and not exported, then write the times of the text file in the same format that the times above are written in. An example of a time is seen here:

**10.45, F L B F2 R D' L B F' R2 D L2 R B L D2 U2 B' F U2 L2 B F', 2020-08-29-7:43 PM**

Every line should represent a new time in the file. If the time is a DNF, you have to specify by adding an extra boolean parameter, if it isn't, then you don't have to specify:

**10.45, F L B F2 R D' L B F' R2 D L2 R B L D2 U2 B' F U2 L2 B F', 2020-08-29-7:43 PM, True***

This feature will be helpful for people who want to change the time a solve was recorded, or for people who want to un-DNF a solve.
### Inspection
If you want to have WCA inspection enabled or disabled, go to settings, and you'll see a checkbutton, if its checked, then inspection is on, if not then it isn't. WCA inspection lasts 15 seconds, so you have 15 seconds to look at your scrambled cube. If you exceed 15 seconds, then you can get a plus 2 or even a DNF, which are both penalties

### Penalties
But, what exactly are penalties ? Penalties happen if your solve wasn't done properly, like for example, if you are one turn away from solving the cube, but you stopped the timer before you solved it, then its a plus 2, but if it was more than 1 turn away from being solved and you stopped the timer, it's a DNF. Plus 2 is self explanitory, it adds two seconds to your time, DNF stands for Did Not Finish, it's the worst possible time you can get, if you have 2 DNF's in one session, the average is DNF. You can DNF / plus 2 a time, by clicking on it in the listbox with all your times, then select the desired penalty. Your time will be automatically DNF'd / plus 2'd if your inspection exceeds 15 seconds.

## Time options
If you need to modify / delete a time, or view a times information, you can enter its options. To do so, you can double click the time, in the times listbox.

### Delete time
If you wish to delete a time, then you can double click it to enter its options, then click the button that says **Delete time**. You can also select the time in the listbox and press the Delete key.

### Display time
If you don't want to see your time while solving, you can have it so that it only displays your time when you stop the timer. To do so, go to settings and un-check the display times checkbutton. Instead of displaying your time, it'll show "..." while you are solving.

### Puzzle type
If you want to include wide moves (r, l, b, u, d) in your solves because you are solving on a big cube, you can change the puzzle type in settings, replace 3x3 with whatever puzzle type you want.

### Scramble length
To change your scramble length, go to settings and change the entry under the "Scramble length" label, whenever your stop the timer, it'll generate a scramble of that size.

### Copy times
Copying your times to your clipboard is easy, just go to settings, and click the **Copy Times** button, it'll surround your worst and best times with parenthesis.

**(5.27), 2.03, (0.65)**

## Mulitphase
If you ever want to time each part of your solve, then you can change your solve multiphase, for example, if your solving method is CFOP, then you would set your multiphase to 4. To change your multiphase, go to settings and change the entry under the label that says "Multiphase". When you are doing a solve and you are done a step of your solving method, then press the space bar. If you go to this multiphase time's options, then you can see the time it took you to do each step of your solve:

![Multiphase time](/Screenshots/

## Keybinds
- e - Export times
- i - Import times
- Space - Start / Stop Timer
- t - Display times in a Time Table
- F11 - Toggle fullscreen
- Escape - Exits fullscreen
- Delete - Deletes the selected time in the listbox 

## License
[MIT](https://choosealicense.com/licenses/mit/)
