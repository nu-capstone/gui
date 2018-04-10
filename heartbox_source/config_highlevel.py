#!/usr/bin/env python
import Tkinter as tk
import tkFont
import ttk
import settings
from PIL import Image, ImageTk
import pdb
import subprocess
import os
import webbrowser
chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'

class config_highlevel:
	def __init__(self): 
		self.path = os.path.dirname(os.path.abspath(__file__))
		config_highlevel = tk.Toplevel()
		config_highlevel.configure(bg = settings.back_color)
		config_highlevel.minsize(width = 900, height = 600)
		config_highlevel.columnconfigure(0, weight = 1)
		config_highlevel.title('HeartBox High-level Configuration')

		self.title_font_size = 8
		self.subtitle_font_size = 6

		self.title_font = tkFont.Font(family = 'Consolas', size = self.title_font_size)
		self.subtitle_font = tkFont.Font(family = 'Consolas', size = self.subtitle_font_size)

		self.create_banner(config_highlevel)
		self.ppg_highLevelControl(config_highlevel)
		self.frame_ppg_LEDOptions(config_highlevel)

	def create_banner(self, master): #menu pane configuration
		img = ImageTk.PhotoImage(Image.open("heart_box_logo.png"))
		self.picture_frame = tk.Frame(master, bd = 0)
		self.picture_frame.grid(row = 0, column = 0, sticky=tk.W+tk.E+tk.N+tk.S)
		self.picture_frame.columnconfigure(0, weight = 1)
		self.picture_frame.columnconfigure(1, weight = 1)
		self.picture_frame.columnconfigure(2, weight = 1)
		self.picture_frame.columnconfigure(3, weight = 1)

		self.panel = tk.Label(self.picture_frame, image = img, padx = 0, pady = 0, bd = 0,
			fg= settings.font_color, bg = settings.back_color)
		self.panel2 = tk.Label(self.picture_frame, image = img, padx = 0, pady = 0, bd = 0,
			fg= settings.font_color, bg = settings.back_color)
		self.panel3 = tk.Label(self.picture_frame, image = img, padx = 0, pady = 0, bd = 0,
			fg= settings.font_color, bg = settings.back_color)
		self.panel4 = tk.Label(self.picture_frame, image = img, padx = 0, pady = 0, bd = 0,
			fg= settings.font_color, bg = settings.back_color)

		self.panel.image = img
		self.panel2.image = img
		self.panel3.image = img
		self.panel4.image = img

		self.panel.grid(row = 0, column = 0, sticky=tk.W+tk.E+tk.N+tk.S)
		self.panel2.grid(row = 0, column = 1, sticky=tk.W+tk.E+tk.N+tk.S)
		self.panel3.grid(row = 0, column = 2, sticky=tk.W+tk.E+tk.N+tk.S)
		self.panel4.grid(row = 0, column = 3, sticky=tk.W+tk.E+tk.N+tk.S)

	def ppg_highLevelControl(self, master): #button for switching into register level
		self.frame_register = tk.Frame(master, bd = 0, bg = settings.back_color)
		self.frame_register.grid(row = 1, column = 0, sticky = tk.W+tk.E+tk.N+tk.S)
		self.frame_register.columnconfigure(0, weight = 4)
		self.frame_register.columnconfigure(1, weight = 1)
		self.panel = tk.Label(self.frame_register, padx = 0, pady = 0, bd = 0,
			fg= settings.font_color, bg = settings.back_color)
		self.panel.grid(row = 0, column = 0)

		self.switchTo_RegisterLevel = tk.Button(self.frame_register, text= "REGISTER LEVEL", 
			height = 1, fg= settings.font_color, bg = settings.back_color, pady = 6)
		self.switchTo_RegisterLevel.config(font=(4))
		self.switchTo_RegisterLevel.grid(row = 0, column = 1, sticky = tk.S, pady = 2)

	def frame_ppg_LEDOptions(self, master): #container for all LED (slotA/B) options
		self.frame_ppg = tk.LabelFrame(master, bd = 3, text = "3 LED's High Level Control",
		 fg= settings.font_color, bg = settings.back_color)
		self.frame_ppg.config(font=(10))
		self.frame_ppg.grid(row = 2, column = 0, pady = 10, sticky = tk.W+tk.E+tk.N+tk.S)
		self.frame_ppg.columnconfigure(0, weight = 1)
		self.frame_ppg.columnconfigure(1, weight = 1)

		self.frame_ppg_left = tk.Frame(self.frame_ppg, bd = 0, bg = settings.back_color)
		self.frame_ppg_right = tk.Frame(self.frame_ppg, bd = 0, bg = settings.back_color)
		self.frame_ppg_left.grid(row = 0, column = 0, sticky = tk.W+tk.E+tk.N+tk.S)
		self.frame_ppg_right.grid(row = 0, column = 1, sticky = tk.W+tk.E+tk.N+tk.S)
		self.frame_ppg_left.columnconfigure(0, weight = 1)
		self.frame_ppg_left.columnconfigure(1, weight = 1)
		self.frame_ppg_left.columnconfigure(2, weight = 1)

		self.frame_ppg_right.columnconfigure(0, weight = 1)
		self.frame_ppg_right.columnconfigure(1, weight = 1)
		self.frame_ppg_right.columnconfigure(2, weight = 1)

		self.sampling_freq_text = tk.Button(self.frame_ppg_left, text = "Sampling Frequency",
			fg= settings.font_color, bg = settings.back_color, activebackground= settings.back_color,
			bd = 0, command= lambda: self.open_adpd103_docs('22'))
		self.sampling_freq_text.grid(row = 0, column = 1, sticky = tk.W)
		self.sampling_freq_spinbox = tk.Spinbox(self.frame_ppg_left, from_ = 1, to = 100, increment =1, 
			width = 5 , fg= settings.font_color, bg = settings.back_color, buttonbackground = settings.back_color)
		self.sampling_freq_spinbox.grid(row = 0, column = 2, sticky = tk.W)

		self.int_average_text = tk.Button(self.frame_ppg_left, text = "Internal Average",
			fg= settings.font_color, bg = settings.back_color, bd = 0, activebackground= settings.back_color, command= lambda: self.open_adpd103_docs('23'))
		self.int_average_text.grid(row = 1, column = 1, sticky = tk.W)
		int_average_slotA = ('1',
			'2',
			'4',
			'8',
			'16', 
			'32',
			'64',
			'128')
		self.default_int_average_slotA = tk.StringVar()

		self.default_int_average_slotA.set(int_average_slotA[0])
		self.slot_mode_A_int_average = tk.OptionMenu(self.frame_ppg_left, self.default_int_average_slotA, *int_average_slotA)
		self.slot_mode_A_int_average["highlightthickness"]=0
		self.slot_mode_A_int_average.configure(fg= settings.font_color, bg = settings.back_color)
		self.slot_mode_A_int_average.grid(row = 1, column = 2, sticky = tk.W)

		self.slot_mode_A_text = tk.Button(self.frame_ppg_right, text = "Slot_Mode A",
			fg= settings.font_color, bg = settings.back_color, bd = 0, activebackground= settings.back_color, command= lambda: self.open_adpd103_docs('19'))
		self.slot_mode_A_text.grid(row = 0, column = 0)
		options_slotA = ('ADPDDrv_SLOT_OFF', 
			'ADPDDrv_4CH_16',
			'ADPDDrv_4CH_32',
			'ADPDDrv_SUM_16',
			'ADPDDrv_SUM_32',
			'ADPDDrv_DIM1_16',
			'ADPDDrv_DIM1_32',			
			'ADPDDrv_DIM2_16',
			'ADPDDrv_DIM2_32',
			'ADPDDrv_PROXIMITY')

		self.default_option_slotA = tk.StringVar()
		self.default_option_slotA.set(options_slotA[0])
		self.slot_mode_A_optionmenu = tk.OptionMenu(self.frame_ppg_right, self.default_option_slotA, *options_slotA)
		self.slot_mode_A_optionmenu.configure(fg= settings.font_color, bg = settings.back_color)
		self.slot_mode_A_optionmenu["highlightthickness"]=0
		self.slot_mode_A_optionmenu.grid(row = 0, column = 1)

		self.slot_mode_B_text = tk.Button(self.frame_ppg_right, text = "Slot_Mode B",
			fg= settings.font_color, bg = settings.back_color, bd = 0, activebackground= settings.back_color, 
			command= lambda: self.open_adpd103_docs('19'))
		self.slot_mode_B_text.grid(row = 1, column = 0)
		options_slotB = ('ADPDDrv_SLOT_OFF', 
			'ADPDDrv_4CH_16',
			'ADPDDrv_4CH_32',
			'ADPDDrv_SUM_16',
			'ADPDDrv_SUM_32',
			'ADPDDrv_DIM1_16',
			'ADPDDrv_DIM1_32',			
			'ADPDDrv_DIM2_16',
			'ADPDDrv_DIM2_32')

		self.default_option_slotB = tk.StringVar()
		self.default_option_slotB.set(options_slotB[0])

		self.slot_mode_B_optionmenu = tk.OptionMenu(self.frame_ppg_right, self.default_option_slotB, *options_slotB)
		self.slot_mode_B_optionmenu.configure(fg= settings.font_color, bg = settings.back_color)
		self.slot_mode_B_optionmenu["highlightthickness"]=0
		self.slot_mode_B_optionmenu.grid(row = 1, column = 1)

		self.frame_slot_A_control(self.frame_ppg)
		self.frame_slot_B_control(self.frame_ppg)
		self.frame_all_LED_currents(self.frame_ppg)

	def frame_slot_A_control(self, master):
		self.frame_slot_A_control = tk.LabelFrame(master, bd = 2, text = "SLOT A CONTROL",
			fg= settings.font_color, bg = settings.back_color)
		self.frame_slot_A_control.grid(row = 1, column = 0, pady = 10, padx = 5, sticky = tk.N + tk.W + tk.E + tk.S)
		self.frame_slot_A_control.columnconfigure(0, weight = 1)
		self.frame_slot_A_control.columnconfigure(1, weight = 1)

		self.frame_slot_A_LED_control(self.frame_slot_A_control)
		self.frame_slot_A_timing_control(self.frame_slot_A_control)

	def frame_slot_B_control(self, master):
		self.frame_slot_B_control = tk.LabelFrame(master, bd = 2, text = "SLOT B CONTROL",
			fg= settings.font_color, bg = settings.back_color)
		self.frame_slot_B_control.grid(row = 1, column = 1, pady = 10, padx = 5, sticky = tk.N + tk.W + tk.E + tk.S)
		self.frame_slot_B_control.columnconfigure(0, weight = 1)
		self.frame_slot_B_control.columnconfigure(1, weight = 1)

		self.frame_slot_B_LED_control(self.frame_slot_B_control)
		self.frame_slot_B_timing_control(self.frame_slot_B_control)

	def frame_slot_A_LED_control(self, master):
		self.frame_slot_A_LED_control = tk.LabelFrame(master, bd = 2, text = "LED Control",
			fg= settings.font_color, bg = settings.back_color)
		self.frame_slot_A_LED_control.grid(row = 0, column = 0, pady = 10, padx = 5, sticky = tk.N + tk.W + tk.E + tk.S)
		self.frame_slot_A_LED_control.columnconfigure(0, weight = 1)
		self.frame_slot_A_LED_control.columnconfigure(1, weight = 1)

		self.frame_slot_A_LED_control_box_A = tk.LabelFrame(self.frame_slot_A_LED_control, 
			bd = 2, fg= settings.font_color, bg = settings.back_color)
		self.frame_slot_A_LED_control_box_A.grid(row = 0, column = 0, pady = 10, padx = 5)

		self.slot_A_LED_text = tk.Button(self.frame_slot_A_LED_control_box_A, text = "LED",
			fg= settings.font_color, bg = settings.back_color, bd = 0, activebackground= settings.back_color, 
			command= lambda: self.open_adpd103_docs('31'))
		self.slot_A_LED_text.grid(row = 0, column = 0)

		options_slotA_LED = ('LED NONE', 'LED 1', 'LED 2', 'LED 3')
		self.default_options_slotA_LED = tk.StringVar()
		self.default_options_slotA_LED.set(options_slotA_LED[0])

		self.slot_A_LED_option_menu = tk.OptionMenu(self.frame_slot_A_LED_control_box_A, self.default_options_slotA_LED, *options_slotA_LED)
		self.slot_A_LED_option_menu.configure(fg= settings.font_color, bg = settings.back_color)
		self.slot_A_LED_option_menu["highlightthickness"] = 0
		self.slot_A_LED_option_menu.grid(row = 0, column = 1, sticky = tk.W+tk.E+tk.N+tk.S)

		self.slot_A_LED_status_text = tk.Label(self.frame_slot_A_LED_control_box_A, text = "LED Status",
			fg= settings.font_color, bg = settings.back_color)
		self.slot_A_LED_status_text.grid(row = 1, column = 0)
		options_slotA_LED_status = ('LED ON', 'LED OFF')
		self.default_options_slotA_LED_status = tk.StringVar()
		self.default_options_slotA_LED_status.set(options_slotA_LED_status[0])

		self.slot_A_LED_status_option_menu = tk.OptionMenu(self.frame_slot_A_LED_control_box_A, self.default_options_slotA_LED_status, *options_slotA_LED_status)
		self.slot_A_LED_status_option_menu.configure(fg= settings.font_color, bg = settings.back_color)
		self.slot_A_LED_status_option_menu["highlightthickness"] = 0
		self.slot_A_LED_status_option_menu.grid(row = 1, column = 1, sticky = tk.W+tk.E+tk.N+tk.S)

		self.num_pulses_slot_A_text = tk.Button(self.frame_slot_A_LED_control_box_A, text = "Number of Pulses",
			fg= settings.font_color, bg = settings.back_color, bd = 0, activebackground= settings.back_color, 
			command= lambda: self.open_adpd103_docs('38'))
		self.num_pulses_slot_A_text.grid(row = 2, column = 0)
		self.num_pulses_slot_A_spinbox = tk.Spinbox(self.frame_slot_A_LED_control_box_A, from_ = 0, to = 100, increment = 1, 
			width = 5, fg= settings.font_color, bg = settings.back_color, buttonbackground = settings.back_color, justify = tk.RIGHT)
		self.num_pulses_slot_A_spinbox.grid(row = 2, column = 1, sticky = tk.W+tk.E+tk.N+tk.S)

		self.frame_slot_A_LED_control_box_B = tk.LabelFrame(self.frame_slot_A_LED_control, bg = settings.back_color)
		self.frame_slot_A_LED_control_box_B.grid(row = 1, column = 0)

		self.slot_A_TIA_gain_text = tk.Button(self.frame_slot_A_LED_control_box_B, text = "TIA Gain",
			fg= settings.font_color, bg = settings.back_color, bd = 0, activebackground= settings.back_color, 
			command= lambda: self.open_adpd103_docs('40'))
		self.slot_A_TIA_gain_text.grid(row = 0, column = 0)
		options_slot_A_TIA_gain = ('25k','50k','100k','200k')

		self.default_options_slot_A_TIA_gain = tk.StringVar()
		self.default_options_slot_A_TIA_gain.set(options_slot_A_TIA_gain[0])

		self.slot_A_TIA_gain_option_menu = tk.OptionMenu(self.frame_slot_A_LED_control_box_B, self.default_options_slot_A_TIA_gain, *options_slot_A_TIA_gain)
		self.slot_A_TIA_gain_option_menu.configure(fg= settings.font_color, bg = settings.back_color)
		self.slot_A_TIA_gain_option_menu["highlightthickness"] = 0
		self.slot_A_TIA_gain_option_menu.grid(row = 0, column = 1)

	def frame_slot_B_LED_control(self, master):
		self.frame_slot_B_LED_control = tk.LabelFrame(master, bd = 2, text = "LED Control",
			fg= settings.font_color, bg = settings.back_color)
		self.frame_slot_B_LED_control.grid(row = 0, column = 0, pady = 10, padx = 5, sticky = tk.N + tk.W + tk.E + tk.S)
		self.frame_slot_B_LED_control.columnconfigure(0, weight = 1)
		self.frame_slot_B_LED_control.columnconfigure(1, weight = 1)

		self.frame_slot_B_LED_control_box_A = tk.LabelFrame(self.frame_slot_B_LED_control, bd = 2,
			fg= settings.font_color, bg = settings.back_color)
		self.frame_slot_B_LED_control_box_A.grid(row = 0, column = 0, pady = 10, padx = 5)

		self.slot_B_LED_text = tk.Button(self.frame_slot_B_LED_control_box_A, text = "LED",
			fg= settings.font_color, bg = settings.back_color, bd = 0, activebackground= settings.back_color, 
			command= lambda: self.open_adpd103_docs('31'))
		self.slot_B_LED_text.grid(row = 0, column = 0)
		options_slotB_LED = ('LED NONE', 'LED 1', 'LED 2', 'LED 3')
		self.default_options_slotB_LED = tk.StringVar()
		self.default_options_slotB_LED.set(options_slotB_LED[0])
		self.slot_B_LED_option_menu = tk.OptionMenu(self.frame_slot_B_LED_control_box_A, self.default_options_slotB_LED, *options_slotB_LED)
		self.slot_B_LED_option_menu.configure(fg= settings.font_color, bg = settings.back_color)
		self.slot_B_LED_option_menu["highlightthickness"] = 0
		self.slot_B_LED_option_menu.grid(row = 0, column = 1, sticky = tk.W+tk.E+tk.N+tk.S)

		self.slot_B_LED_status_text = tk.Label(self.frame_slot_B_LED_control_box_A, text = "LED Status",
			fg= settings.font_color, bg = settings.back_color)
		self.slot_B_LED_status_text.grid(row = 1, column = 0)
		options_slotB_LED_status = ('LED ON', 'LED OFF')
		self.default_options_slotB_LED_status = tk.StringVar()
		self.default_options_slotB_LED_status.set(options_slotB_LED_status[0])

		self.slot_B_LED_status_option_menu = tk.OptionMenu(self.frame_slot_B_LED_control_box_A, self.default_options_slotB_LED_status, *options_slotB_LED_status)
		self.slot_B_LED_status_option_menu.configure(fg= settings.font_color, bg = settings.back_color)
		self.slot_B_LED_status_option_menu["highlightthickness"] = 0
		self.slot_B_LED_status_option_menu.grid(row = 1, column = 1, sticky = tk.W+tk.E+tk.N+tk.S)

		self.num_pulses_slot_B_text = tk.Button(self.frame_slot_B_LED_control_box_A, text = "Number of Pulses",
			fg= settings.font_color, bg = settings.back_color, bd = 0, activebackground= settings.back_color, 
			command= lambda: self.open_adpd103_docs('38'))
		self.num_pulses_slot_B_text.grid(row = 2, column = 0)
		self.num_pulses_slot_B_spinbox = tk.Spinbox(self.frame_slot_B_LED_control_box_A, from_ = 0, to = 100, increment = 1,
		 width = 5, fg= settings.font_color, bg = settings.back_color, buttonbackground = settings.back_color, justify = tk.RIGHT)
		self.num_pulses_slot_B_spinbox.grid(row = 2, column = 1, sticky = tk.W+tk.E+tk.N+tk.S)

		self.frame_slot_B_LED_control_box_B = tk.LabelFrame(self.frame_slot_B_LED_control, bg = settings.back_color)
		self.frame_slot_B_LED_control_box_B.grid(row = 1, column = 0)

		self.slot_B_TIA_gain_text = tk.Button(self.frame_slot_B_LED_control_box_B, text = "TIA Gain",
			fg= settings.font_color, bg = settings.back_color, bd = 0, activebackground= settings.back_color, 
			command= lambda: self.open_adpd103_docs('40'))
		self.slot_B_TIA_gain_text.grid(row = 0, column = 0)
		options_slot_B_TIA_gain = ('25k','50k','100k','200k')

		self.default_options_slot_B_TIA_gain = tk.StringVar()
		self.default_options_slot_B_TIA_gain.set(options_slot_B_TIA_gain[0])

		self.slot_B_TIA_gain_option_menu = tk.OptionMenu(self.frame_slot_B_LED_control_box_B, self.default_options_slot_B_TIA_gain, *options_slot_B_TIA_gain)
		self.slot_B_TIA_gain_option_menu.configure(fg= settings.font_color, bg = settings.back_color)
		self.slot_B_TIA_gain_option_menu["highlightthickness"] = 0
		self.slot_B_TIA_gain_option_menu.grid(row = 0, column = 1)
	
	def frame_slot_A_timing_control(self,master):
		self.frame_slot_A_timing_control = tk.LabelFrame(master, bd = 2, text = "Timing Control",
			fg= settings.font_color, bg = settings.back_color)
		self.frame_slot_A_timing_control.grid(row = 0, column = 1, pady = 10, padx = 5, sticky=tk.W+tk.E+tk.N+tk.S)
		self.frame_slot_A_timing_control.columnconfigure(0, weight = 3)
		self.frame_slot_A_timing_control.columnconfigure(1, weight = 1)

		self.AFE_width_slot_A_text = tk.Button(self.frame_slot_A_timing_control, text = "AFE Width (us)",
			fg= settings.font_color, bg = settings.back_color, bd = 0, activebackground= settings.back_color, 
			command= lambda: self.open_adpd103_docs('19'))
		self.AFE_width_slot_A_text.grid(row = 0, column = 0)
		self.AFE_width_slot_A_spinbox = tk.Spinbox(self.frame_slot_A_timing_control, from_ = 0, to = 100, increment = 1,
			width = 5, fg= settings.font_color, bg = settings.back_color, buttonbackground = settings.back_color, justify = tk.RIGHT)
		self.AFE_width_slot_A_spinbox.grid(row = 0, column = 1, sticky = tk.W+tk.E)

		self.pulse_width_slot_A_text = tk.Label(self.frame_slot_A_timing_control, text = "Pulse Width (us)",
			fg= settings.font_color, bg = settings.back_color)
		self.pulse_width_slot_A_text.grid(row = 1, column = 0)
		self.pulse_width_slot_A_spinbox = tk.Spinbox(self.frame_slot_A_timing_control, from_ = 0, to = 100, increment = 1, 
			width = 5, fg= settings.font_color, bg = settings.back_color, buttonbackground = settings.back_color, justify = tk.RIGHT)
		self.pulse_width_slot_A_spinbox.grid(row = 1, column = 1, sticky = tk.W+tk.E)

		self.pulse_offset_slot_A_text = tk.Label(self.frame_slot_A_timing_control, text = "Pulse Offset (us)",
			fg= settings.font_color, bg = settings.back_color)
		self.pulse_offset_slot_A_text.grid(row = 2, column = 0)
		self.pulse_offset_slot_A_spinbox = tk.Spinbox(self.frame_slot_A_timing_control, from_ = 0, to = 100, increment = 1, 
			width = 5, fg= settings.font_color, bg = settings.back_color, buttonbackground = settings.back_color, justify = tk.RIGHT)
		self.pulse_offset_slot_A_spinbox.grid(row = 2, column = 1, sticky = tk.W+tk.E)

		self.AFE_offset_slot_A_text = tk.Label(self.frame_slot_A_timing_control, text = "AFE Offset (us)",
			fg= settings.font_color, bg = settings.back_color)
		self.AFE_offset_slot_A_text.grid(row = 3, column = 0)
		self.AFE_offset_slot_A_spinbox = tk.Spinbox(self.frame_slot_A_timing_control, from_ = 0, to = 100, increment = 1,
			width = 5, fg= settings.font_color, bg = settings.back_color, buttonbackground = settings.back_color, justify = tk.RIGHT)
		self.AFE_offset_slot_A_spinbox.grid(row = 3, column = 1, sticky = tk.W+tk.E)

		self.fine_AFE_offset_slot_A_text = tk.Label(self.frame_slot_A_timing_control, text = "AFE Fine Offset (ns)",
			fg= settings.font_color, bg = settings.back_color)
		self.fine_AFE_offset_slot_A_text.grid(row = 4, column = 0)
		self.fine_AFE_offset_slot_A_spinbox = tk.Spinbox(self.frame_slot_A_timing_control, from_ = 0.00, to = 1000.00, increment = 31.25, 
			width = 5, fg= settings.font_color, bg = settings.back_color, format = '%.2f',
			buttonbackground = settings.back_color, justify = tk.RIGHT)
		self.fine_AFE_offset_slot_A_spinbox.grid(row = 4, column = 1, sticky = tk.W+tk.E)

	def frame_slot_B_timing_control(self,master):
		self.frame_slot_B_timing_control = tk.LabelFrame(master, bd = 2, text = "Timing Control",
			fg= settings.font_color, bg = settings.back_color)
		self.frame_slot_B_timing_control.grid(row = 0, column = 1, pady = 10, padx = 5, sticky=tk.W+tk.E+tk.N+tk.S)
		self.frame_slot_B_timing_control.columnconfigure(0, weight = 3)
		self.frame_slot_B_timing_control.columnconfigure(1, weight = 1)

		self.AFE_width_slot_B_text = tk.Label(self.frame_slot_B_timing_control, text = "AFE Width (us)",
			fg= settings.font_color, bg = settings.back_color)
		self.AFE_width_slot_B_text.grid(row = 0, column = 0)
		self.AFE_width_slot_B_spinbox = tk.Spinbox(self.frame_slot_B_timing_control, from_ = 0, to = 100, increment = 1,
			width = 5, fg= settings.font_color, bg = settings.back_color, buttonbackground = settings.back_color, justify = tk.RIGHT)
		self.AFE_width_slot_B_spinbox.grid(row = 0, column = 1, sticky = tk.W+tk.E)

		self.pulse_width_slot_B_text = tk.Label(self.frame_slot_B_timing_control, text = "Pulse Width (us)",
			fg= settings.font_color, bg = settings.back_color)
		self.pulse_width_slot_B_text.grid(row = 1, column = 0)
		self.pulse_width_slot_B_spinbox = tk.Spinbox(self.frame_slot_B_timing_control, from_ = 0, to = 100, increment = 1, 
			width = 5, fg= settings.font_color, bg = settings.back_color, buttonbackground = settings.back_color, justify = tk.RIGHT)
		self.pulse_width_slot_B_spinbox.grid(row = 1, column = 1, sticky = tk.W+tk.E)

		self.pulse_offset_slot_B_text = tk.Label(self.frame_slot_B_timing_control, text = "Pulse Offset (us)",
			fg= settings.font_color, bg = settings.back_color)
		self.pulse_offset_slot_B_text.grid(row = 2, column = 0)
		self.pulse_offset_slot_B_spinbox = tk.Spinbox(self.frame_slot_B_timing_control, from_ = 0, to = 100, increment = 1,
			width = 5, fg= settings.font_color, bg = settings.back_color, buttonbackground = settings.back_color, justify = tk.RIGHT)
		self.pulse_offset_slot_B_spinbox.grid(row = 2, column = 1, sticky = tk.W+tk.E)

		self.AFE_offset_slot_B_text = tk.Label(self.frame_slot_B_timing_control, text = "AFE Offset (us)",
			fg= settings.font_color, bg = settings.back_color)
		self.AFE_offset_slot_B_text.grid(row = 3, column = 0)
		self.AFE_offset_slot_B_spinbox = tk.Spinbox(self.frame_slot_B_timing_control, from_ = 0, to = 100, increment = 1,
			width = 5, fg= settings.font_color, bg = settings.back_color, buttonbackground = settings.back_color, justify = tk.RIGHT)
		self.AFE_offset_slot_B_spinbox.grid(row = 3, column = 1, sticky = tk.W+tk.E)

		self.AFE_fine_offset_slot_B_text = tk.Label(self.frame_slot_B_timing_control, text = "AFE Fine Offset (ns)",
			fg= settings.font_color, bg = settings.back_color)
		self.AFE_fine_offset_slot_B_text.grid(row = 4, column = 0)
		self.AFE_fine_offset_slot_B_spinbox = tk.Spinbox(self.frame_slot_B_timing_control, from_ = 0.00, to = 1000.00, increment = 31.25,
			width = 5, fg= settings.font_color, bg = settings.back_color, format = '%.2f',
			buttonbackground = settings.back_color, justify = tk.RIGHT)
		self.AFE_fine_offset_slot_B_spinbox.grid(row = 4, column = 1, sticky = tk.W+tk.E)

	def frame_all_LED_currents(self, master):
		self.frame_all_LED_currents = tk.LabelFrame(master, bd = 0, 
			fg= settings.font_color, bg = settings.back_color)
		self.frame_all_LED_currents.grid(row = 5, column = 0, columnspan = 2, 
			sticky = tk.W+tk.E+tk.N+tk.S)
		self.frame_all_LED_currents.columnconfigure(0, weight=1)
		self.frame_all_LED_currents.columnconfigure(1, weight=1)
		self.frame_all_LED_currents.columnconfigure(2, weight=1)
		self.frame_all_LED_currents.columnconfigure(3, weight=1)
		self.frame_all_LED_currents.columnconfigure(4, weight=1)

		self.frame_LED_1_current(self.frame_all_LED_currents)
		self.frame_LED_2_current(self.frame_all_LED_currents)
		self.frame_LED_3_current(self.frame_all_LED_currents)

		self.apply_ppg_changes_high_level = tk.Button(self.frame_all_LED_currents, text = "Apply",
		 fg= settings.font_color, bg = settings.back_color, padx = 10, pady = 10, command = self.open_rickroll)
		self.apply_ppg_changes_high_level.config(font=(10))
		self.apply_ppg_changes_high_level.grid(row = 0, column = 3)

	def frame_LED_1_current(self, master):
		self.frame_LED_1_current = tk.LabelFrame(master, text = "LED 1 Current",
			fg= settings.font_color, bg = settings.back_color)
		self.frame_LED_1_current.grid(row = 0, column = 0, pady = 10, padx = 5)

		self.frame_LED_1_coarse_scale = tk.Frame(self.frame_LED_1_current, bg = settings.back_color)
		self.frame_LED_1_coarse_scale.grid(row = 0, column = 0)

		self.LED_1_I_LED_coarse_text = tk.Label(self.frame_LED_1_coarse_scale, text = "I_LED Coarse",
			fg= settings.font_color, bg = settings.back_color)
		self.LED_1_I_LED_coarse_text.grid(row = 0, column = 0)
		options_LED_1_I_LED_coarse = ('25', 
			'40', 
			'55',
			'70', 
			'85',
			'100', 
			'115',
			'130', 
			'145',
			'160', 
			'175',
			'190', 
			'205',
			'220', 
			'235',
			'250')

		self.default_options_LED_1_I_LED_coarse= tk.StringVar()
		self.default_options_LED_1_I_LED_coarse.set(options_LED_1_I_LED_coarse[0])

		self.LED_1_I_LED_coarse_option_menu = tk.OptionMenu(self.frame_LED_1_coarse_scale, self.default_options_LED_1_I_LED_coarse, 
			*options_LED_1_I_LED_coarse)
		self.LED_1_I_LED_coarse_option_menu.configure(fg= settings.font_color, bg = settings.back_color)
		self.LED_1_I_LED_coarse_option_menu["highlightthickness"] = 0
		self.LED_1_I_LED_coarse_option_menu.grid(row = 0, column = 1)

		self.LED_1_scale_factor_text = tk.Label(self.frame_LED_1_coarse_scale, text = "Scale Factor",
			fg= settings.font_color, bg = settings.back_color)
		self.LED_1_scale_factor_text.grid(row = 1, column = 0)

		options_LED_1_scale_factor = ('40%', '100%')
		self.default_options_LED_1_scale_factor= tk.StringVar()
		self.default_options_LED_1_scale_factor.set(options_LED_1_scale_factor[0])
		self.LED_1_scale_factor_option_menu = tk.OptionMenu(self.frame_LED_1_coarse_scale, self.default_options_LED_1_scale_factor, 
			*options_LED_1_scale_factor)
		self.LED_1_scale_factor_option_menu.configure(fg= settings.font_color, bg = settings.back_color)
		self.LED_1_scale_factor_option_menu["highlightthickness"] = 0
		self.LED_1_scale_factor_option_menu.grid(row = 1, column = 1)

		self.LED_1_scale = tk.Scale(self.frame_LED_1_current, orient=tk.HORIZONTAL, sliderlength = 15, 
			fg= settings.font_color, bg = settings.back_color, activebackground = settings.back_color)
		self.LED_1_scale.grid(row = 2 , column = 0)
		self.LED_1_scale["highlightthickness"] = 0

		self.frame_LED_1_final_I_LED_field = tk.LabelFrame(self.frame_LED_1_current, bd = 0,
		 fg= settings.font_color, bg = settings.back_color)
		self.frame_LED_1_final_I_LED_field.grid(row = 3 , column = 0)
		self.LED_1_final_I_LED_text = tk.Label(self.frame_LED_1_final_I_LED_field, 
			text = "Final I_LED", fg= settings.font_color, bg = settings.back_color)

		self.LED_1_final_I_LED_text.grid(row = 0, column = 0)
		self.LED_1_final_I_LED_entry = tk.Entry(self.frame_LED_1_final_I_LED_field, width = 10,
			fg= settings.font_color, bg = settings.back_color)
		self.LED_1_final_I_LED_entry.grid(row = 0, column = 1)
		self.LED_1_mA_text = tk.Label(self.frame_LED_1_final_I_LED_field, text = "mA",
			fg= settings.font_color, bg = settings.back_color)
		self.LED_1_mA_text.grid(row = 0, column = 2)

	def frame_LED_2_current(self, master):
		self.frame_LED_2_current = tk.LabelFrame(master, text = "LED 2 Current",
			fg= settings.font_color, bg = settings.back_color)
		self.frame_LED_2_current.grid(row = 0, column =  1, pady = 10, padx = 5)

		self.frame_LED_2_coarse_scale = tk.Frame(self.frame_LED_2_current, bg = settings.back_color)
		self.frame_LED_2_coarse_scale.grid(row = 0, column = 0)

		self.LED_2_I_LED_coarse_text = tk.Label(self.frame_LED_2_coarse_scale, text = "I_LED Coarse",
			fg= settings.font_color, bg = settings.back_color)
		self.LED_2_I_LED_coarse_text.grid(row = 0, column = 0)
		options_LED_2_I_LED_coarse = ('25', 
			'40', 
			'55',
			'70', 
			'85',
			'100', 
			'115',
			'130', 
			'145',
			'160', 
			'175',
			'190', 
			'205',
			'220', 
			'235',
			'250')

		self.default_options_LED_2_I_LED_coarse= tk.StringVar()
		self.default_options_LED_2_I_LED_coarse.set(options_LED_2_I_LED_coarse[0])

		self.LED_2_I_LED_coarse_option_menu = tk.OptionMenu(self.frame_LED_2_coarse_scale, 
			self.default_options_LED_2_I_LED_coarse, *options_LED_2_I_LED_coarse)
		self.LED_2_I_LED_coarse_option_menu.configure(fg= settings.font_color, bg = settings.back_color)
		self.LED_2_I_LED_coarse_option_menu["highlightthickness"] = 0
		self.LED_2_I_LED_coarse_option_menu.grid(row = 0, column = 1)

		self.LED_2_scale_factor_text = tk.Label(self.frame_LED_2_coarse_scale, text = "Scale Factor",
			fg= settings.font_color, bg = settings.back_color)
		self.LED_2_scale_factor_text.grid(row = 1, column = 0)
		options_LED_2_scale_factor = ('40%', '100%')
		self.default_options_LED_2_scale_factor= tk.StringVar()
		self.default_options_LED_2_scale_factor.set(options_LED_2_scale_factor[0])

		self.LED_2_scale_factor_option_menu = tk.OptionMenu(self.frame_LED_2_coarse_scale, self.default_options_LED_2_scale_factor, 
			*options_LED_2_scale_factor)
		self.LED_2_scale_factor_option_menu.configure(fg= settings.font_color, bg = settings.back_color)
		self.LED_2_scale_factor_option_menu["highlightthickness"] = 0
		self.LED_2_scale_factor_option_menu.grid(row = 1, column = 1)

		self.LED_2_scale = tk.Scale(self.frame_LED_2_current, orient=tk.HORIZONTAL, 
			fg= settings.font_color, bg = settings.back_color, sliderlength = 15,
			activebackground = settings.back_color)
		self.LED_2_scale["highlightthickness"] = 0
		self.LED_2_scale.grid(row = 2 , column = 0)

		self.frame_LED_2_final_I_LED_field = tk.LabelFrame(self.frame_LED_2_current, bd = 0,
			fg= settings.font_color, bg = settings.back_color)
		self.frame_LED_2_final_I_LED_field.grid(row = 3 , column = 0)

		self.LED_2_final_I_LED_text = tk.Label(self.frame_LED_2_final_I_LED_field, text = "Final I_LED",
			fg= settings.font_color, bg = settings.back_color)

		self.LED_2_final_I_LED_text.grid(row = 0, column = 0)
		self.LED_2_final_I_LED_entry = tk.Entry(self.frame_LED_2_final_I_LED_field, width = 10,
		 fg= settings.font_color, bg = settings.back_color)
		self.LED_2_final_I_LED_entry.grid(row = 0, column = 1)
		self.LED_2_mA_text = tk.Label(self.frame_LED_2_final_I_LED_field, text = "mA",
			fg= settings.font_color, bg = settings.back_color)
		self.LED_2_mA_text.grid(row = 0, column = 2)

	def frame_LED_3_current(self, master):
		self.frame_LED_3_current = tk.LabelFrame(master, bd = 2, text = "LED 3 Current",
			fg= settings.font_color, bg = settings.back_color)
		self.frame_LED_3_current.grid(row = 0, column = 2, pady = 10, padx = 5)

		self.frame_LED_3_coarse_scale = tk.Frame(self.frame_LED_3_current, bg = settings.back_color)
		self.frame_LED_3_coarse_scale.grid(row = 0, column = 0)

		self.LED_3_I_LED_coarse_text = tk.Label(self.frame_LED_3_coarse_scale, text = "I_LED Coarse",
			fg= settings.font_color, bg = settings.back_color)
		self.LED_3_I_LED_coarse_text.grid(row = 0, column = 0)
		options_LED_3_I_LED_coarse = ('25', 
			'40', 
			'55',
			'70', 
			'85',
			'100', 
			'115',
			'130', 
			'145',
			'160', 
			'175',
			'190', 
			'205',
			'220', 
			'235',
			'250')

		self.default_options_LED_3_I_LED_coarse= tk.StringVar()
		self.default_options_LED_3_I_LED_coarse.set(options_LED_3_I_LED_coarse[0])

		self.LED_3_I_LED_coarse_option_menu = tk.OptionMenu(self.frame_LED_3_coarse_scale, self.default_options_LED_3_I_LED_coarse, 
			*options_LED_3_I_LED_coarse)
		self.LED_3_I_LED_coarse_option_menu.configure(fg= settings.font_color, bg = settings.back_color)
		self.LED_3_I_LED_coarse_option_menu["highlightthickness"] = 0
		self.LED_3_I_LED_coarse_option_menu.grid(row = 0, column = 1)

		self.LED_3_scale_factor_text = tk.Label(self.frame_LED_3_coarse_scale, text = "Scale Factor",
			fg= settings.font_color, bg = settings.back_color)
		self.LED_3_scale_factor_text.grid(row = 1, column = 0)
		options_LED_3_scale_factor = ('40%', '100%')
		self.default_options_LED_3_scale_factor= tk.StringVar()
		self.default_options_LED_3_scale_factor.set(options_LED_3_scale_factor[0])

		self.LED_3_scale_factor_option_menu = tk.OptionMenu(self.frame_LED_3_coarse_scale, self.default_options_LED_3_scale_factor, 
			*options_LED_3_scale_factor)
		self.LED_3_scale_factor_option_menu.configure(fg= settings.font_color, bg = settings.back_color)
		self.LED_3_scale_factor_option_menu["highlightthickness"] = 0
		self.LED_3_scale_factor_option_menu.grid(row = 1, column = 1)

		self.LED_3_scale = tk.Scale(self.frame_LED_3_current, orient=tk.HORIZONTAL, 
			fg= settings.font_color, bg = settings.back_color, sliderlength = 15,
			activebackground = settings.back_color)
		self.LED_3_scale["highlightthickness"] = 0
		self.LED_3_scale.grid(row = 2 , column = 0)

		self.frame_LED_3_final_I_LED_field = tk.LabelFrame(self.frame_LED_3_current, bd = 0, 
			fg= settings.font_color, bg = settings.back_color)
		self.frame_LED_3_final_I_LED_field.grid(row = 3 , column = 0)
		self.LED_3_final_I_LED_text = tk.Label(self.frame_LED_3_final_I_LED_field, text = "Final I_LED", 
			fg= settings.font_color, bg = settings.back_color)

		self.LED_3_final_I_LED_text.grid(row = 0, column = 0)
		self.LED_3_final_I_LED_entry = tk.Entry(self.frame_LED_3_final_I_LED_field, 
			width = 10, fg= settings.font_color, bg = settings.back_color)
		self.LED_3_final_I_LED_entry.grid(row = 0, column = 1)
		self.LED_3_mA_text = tk.Label(self.frame_LED_3_final_I_LED_field, text = "mA",
			fg= settings.font_color, bg = settings.back_color)

		self.LED_3_mA_text.grid(row = 0, column = 2, sticky = tk.E)

	def open_adpd103_docs(self, pageString):
		pdf_link = "file:///" + self.path + "/ADPD105-106-107.pdf#page=" + pageString
		webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(pdf_link)

	def open_rickroll(self):
		webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
