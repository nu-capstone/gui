import Tkinter as tk
import tkFont
import ttk
import settings
from PIL import Image, ImageTk
import pdb

class config_highlevel:
	def __init__(self): 
		config_highlevel = tk.Toplevel()
		config_highlevel.configure(bg = settings.back_color)
		config_highlevel.minsize(width = 900, height = 600)
		config_highlevel.columnconfigure(0, weight = 1)

		self.title_font_size = 8
		self.subtitle_font_size = 6 

		self.title_font = tkFont.Font(family = 'Consolas', size = self.title_font_size)
		self.subtitle_font = tkFont.Font(family = 'Consolas', size = self.subtitle_font_size)
		self.led_control_registers(config_highlevel)

	def led_control_registers(self, master):
		self.led_control_registers = tk.LabelFrame(master, text = "LED CONTROL REGISTERS", 
			fg= settings.font_color, bg = settings.back_color)
		self.led_control_registers.grid(row = 0, column = 0, 
			sticky = tk.N + tk.S + tk.W + tk.E)

		self.reg0x14
		self.reg0x22
		self.reg0x23
		self.reg0x24
		self.reg0x25
		self.reg0x30
		self.reg0x31
		self.reg0x34
		self.reg0x35
		self.reg0x36

	def afe_global_config_registers(self, master):
		self.afe_global_config_registers = tk.LabelFrame(master, text = "LED CONTROL REGISTERS", 
			fg= settings.font_color, bg = settings.back_color)
		self.afe_global_config_registers.grid(row = 1, column = 0, 
			sticky = tk.N + tk.S + tk.W + tk.E)

		self.reg0x37
		self.reg0x3C
		self.reg0x54
		self.reg0x58
		self.reg0x5A
		#slot A
		self.reg0x39
		self.reg0x42
		self.reg0x43
		self.reg0x55
		self.reg0x5A
		#slot B
		self.reg0x3B
		self.reg0x44
		self.reg0x45
		self.reg0x58


	def system_registers(self, master):

		self.reg0x00
		self.reg0x01
		self.reg0x02
		self.reg0x06
		self.reg0x08
		self.reg0x09
		self.reg0x0A
		self.reg0x0B
		self.reg0x0D
		self.reg0x0F
		self.reg0x10
		self.reg0x11
		self.reg0x38
		self.reg0x4B
		self.reg0x4D
		self.reg0x4E
		self.reg0x4F
		self.reg0x50
		self.reg0x5F

	def adc_registers(self, master):

		self.reg0x12
		self.reg0x15
		self.reg0x18
		self.reg0x19
		self.reg0x1A
		self.reg0x1B
		self.reg0x1E
		self.reg0x1F
		self.reg0x02
		self.reg0x21