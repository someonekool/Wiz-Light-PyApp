import tkinter as tk
from tkinter import colorchooser as cc
from tkinter import messagebox as mb
import datetime
import logging
import asyncio
from commands import cmds as cmds
import os

if not os.path.exists('logs'):
    os.makedirs('logs', exist_ok=True)
    print('Created logs folder')

else:
    pass

if not os.path.isfile('logs/actions.log'):
    with open('logs/actions.log', 'w') as f:
        print('Created actions.log file')
else:
    pass



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler('logs/actions.log', encoding='utf-8')
fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fh.setFormatter(fmt)
logger.addHandler(fh)

logger.propagate = False

time = datetime.datetime

# Stops TK from opening random window
root = tk.Tk()
root.withdraw()



def notify(title, message):
    mb.showinfo(title, message)
    logger.info(f'{message}')

def error(title, message):
    mb.showerror(title, message)
    logger.error(f'{message}')


# noinspection PyTypeChecker
def async_red():  # Runs red command from cmds.py asynchronously
    """Runs red command from cmds.py asynchronously"""
    red = asyncio.run(cmds.red())

    # Checks if the light is already red
    if red:
        notify('Light Bulb turned red', 'Light Bulb turned red')
    elif not red:
        error('Light Bulb is already red', 'Light Bulb is already red')


# noinspection PyTypeChecker
def async_green():  # Runs green command from cmds.py asynchronously
    """Runs green command from cmds.py asynchronously"""
    green = asyncio.run(cmds.green())
    # Checks if the light is already green
    if green:
        notify('Light Bulb turned green', 'Light Bulb turned green')
    elif not green:
        error('Light Bulb is already green', "Light Bulb is already green")


# noinspection PyTypeChecker
def async_blue():
    """Runs blue command from cmds.py asynchronously"""
    blue = asyncio.run(cmds.blue())
    if blue:
        notify('Light Bulb turned blue', 'Light Bulb turned blue')
    elif not blue:
        error('Light Bulb is already blue', 'Light Bulb is already blue')


# noinspection PyTypeChecker
def async_turn_off():
    """Runs turn_off command from cmds.py asynchronously"""
    off = asyncio.run(cmds.turn_off())
    if off:
        notify('Light Bulb turned off', 'Light Bulb turned off')
    elif not off:
        error('Light Bulb is already off', 'Light Bulb is already off')


def async_get_ip():
    """Runs get_if_ip command from cmds.py asynchronously"""
    conf = asyncio.run(cmds.bulb_config())
    return conf


# noinspection PyTypeChecker
def async_turn_on():
    turn_on = asyncio.run(cmds.turn_on())
    if turn_on:
        notify('Light Bulb turned on', 'Light Bulb turned on')
    elif not turn_on:
        error('Light Bulb is already on', 'Light Bulb is already on')



# noinspection PyTypeChecker
def async_custom_color(r, g, b): # Sets custom color based on rgb values
    color_1 = asyncio.run(cmds.custom_color(r, g, b)) # Calls custom_color function from cmds.py
    # Checks if the color has already been set
    if color_1:
        notify('Custom Color', 'Custom Color set successfully')
    elif not color_1:
        error('Custom Color', 'Custom Color already set')





# Main Window
class Window(tk.Tk):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.title('Light Bulb Controller')
        self.geometry('500x865')
        self.bind('<FocusOut>', lambda e: self.title('Where you go???'))
        self.bind('<FocusIn>', lambda a: self.title('Light Bulb Controller'))
        self.label = tk.Label(self, text='Light Bulb Controller', font=('Arial', 24))
        self.label.config(width=20)
        self.label.pack()

        red = self.button_r = tk.Button(self, text='Red', command= async_red)
        red.place(x=20, y=100)
        red.config(height=5, width=15,bg='red')
        red.bind('<Enter>', lambda e: red.config(bg='darkred'))
        red.bind('<Leave>', lambda e: red.config(bg='red'))

        green = self.button_g = tk.Button(self, text='Green', command= async_green)
        green.place(x=185, y=100)
        green.config(height=5, width=15)
        green.config(bg='green')
        green.bind('<Enter>', lambda e: green.config(bg='darkgreen'))
        green.bind('<Leave>', lambda e: green.config(bg='green'))

        blue = self.button_b = tk.Button(self, text='Blue', command= async_blue)
        blue.place(x=350, y=100)
        blue.config(bg='blue')
        blue.config(height=5, width=15)
        blue.bind('<Enter>', lambda e: blue.config(bg='darkblue'))
        blue.bind('<Leave>', lambda e: blue.config(bg='blue'))

        turn_on = self.button = tk.Button(self, text='On', command=async_turn_on)
        turn_on.place(x=102.5, y=300)
        turn_on.config(height=5, width=15)

        turn_off = self.button = tk.Button(self, text='Off', command= async_turn_off)
        turn_off.place(x=267.5, y=300)
        turn_off.config(height=5, width=15)


        color_picker = self.button = tk.Button(self, text='Color Picker', command= ColorPicker().deiconify)
        color_picker.place(x=100, y=500)
        color_picker.config(height=5, width=15)


# Color Picker Window
class ColorPicker(tk.Toplevel):
    """Color Picker Window"""
    def __init__(self):
        super().__init__()
        self.title('Color Picker')
        self.geometry('500x500')
        lab = self.label = tk.Label(self, text='Color Picker', font=('Arial', 24))
        lab.config(width=20)
        lab.pack()
        self.withdraw()

        r_scale = self.red_scale = tk.Scale(self, from_=0, to=255, orient='horizontal', label='Red', cursor='tcross', activebackground='red')
        r_scale.config(bg='red', fg='white',sliderlength=10,  width=10, relief='flat')
        r_scale.place(x=10, y=125)

        b_scale = self.blue_scale = tk.Scale(self, from_=0, to=255, orient='horizontal', label='Blue', cursor='tcross')
        b_scale.config(bg='blue', fg='white',sliderlength=10,  width=10, relief='flat', cursor='tcross')
        b_scale.place(x=200, y=125)

        g_scale = self.green_scale = tk.Scale(self, from_=0, to=255, orient='horizontal', label='Green', cursor='tcross')
        g_scale.config(bg='green', fg='white',sliderlength=10,  width=10, relief='flat')
        g_scale.place(x=380, y=125)

        confirm = self.sendcolor = tk.Button(self, text='Confirm', command=lambda: async_custom_color(*self.get_color_rgb()))
        confirm.place(x=10, y=400)
        confirm.config(height=5, width=15)

        exit_butt = self.exit = tk.Button(self, text='Close', command=self.withdraw)
        exit_butt.place(x=200, y=400)
        exit_butt.config(height=5, width=15)




        pick_col = self.pb = tk.Button(self, text='Pick Color', command= lambda:  async_custom_color(*self.csc()))
        pick_col.place(x=380, y=400)
        pick_col.config(height=5, width=15)



    @staticmethod
    def csc(): # Prompts user with color picker and returns rgb values
        color = cc.askcolor()
        rgb = [color[0]]
        print(rgb)
        red = rgb[0][0]
        green = rgb[0][1]
        blue = rgb[0][2]
        print(red, green, blue)
        return red, green, blue



    def get_color_rgb(self): # Returns rgb values from scales
        red = self.red_scale.get()
        blue = self.blue_scale.get()
        green = self.green_scale.get()
        return red, green, blue




def main():
    print(f'Instance created at {time.now().strftime('%c')}')
    logger.info(f'Instance created\n')
    Window().mainloop()
    ColorPicker().mainloop()



if __name__ == '__main__':
    main()