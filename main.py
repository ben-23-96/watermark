from tkinter import Tk, ttk
from gui import WaterMarkGUI

window = Tk()

style = ttk.Style()
style.theme_use('xpnative')

gui = WaterMarkGUI(window)
gui.load_gui()

window.mainloop()
