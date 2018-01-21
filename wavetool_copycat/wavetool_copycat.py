#!/usr/bin/env python
import Tkinter as tk
from PIL import Image

class Application:
	def __init__(self, master): 
		master.title('Wavetool Copycat')
		self.createMenu(root)
		self.ppg_highLevelControl(root)
		self.frame_ppg_ledOptions(root)


	def createMenu(self, master): #menu pane configuration
		menubar = tk.Menu(master) 
		master.config(menu=menubar)

		menubar.add_command(label="File")
		menubar.add_command(label="View")
		menubar.add_command(label="Tools")
		menubar.add_command(label="Help")

	def ppg_highLevelControl(self, master): #button for switching into register level
		self.switchTo_RegisterLevel = tk.Button(master, text="Go to Register Level")
		self.switchTo_RegisterLevel.grid(row = 0, column = 1)

	def frame_ppg_ledOptions(self, master): #container for all led (slotA/B) options
		self.frame_ppg = tk.Frame(master, bd = 3)
		self.frame_ppg.grid(row = 1, column = 0, columnspan = 2)
		self.frame_ppg.grid(row = 1, column = 0, columnspan = 2)
		self.frame_ppg_text = tk.Label(self.frame_ppg, text = "3 LED's High Level Control")

root = tk.Tk()
app = Application(root)
root.mainloop()