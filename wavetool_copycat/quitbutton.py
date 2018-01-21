#!/usr/bin/env python
import Tkinter as tk

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.createWidgets()

	def createWidgets(self):
		self.quitButton = tk.Button(self, text='Quit', command=self.quit)
		self.quitButton2 = tk.Button(self, text='Quit', command=self.quit)
		self.quitButton.grid(row=0, column=0)
		self.quitButton.grid(row=1, column=0)
		self.quitButton2.grid(row=0, column=1)

	def createMenu(self):
		self.menu

class Application2(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		self.createWidgets()

	def createWidgets(self):
		self.quitButton = tk.Button(self, text='Quit', command=self.quit)
		self.quitButton2 = tk.Button(self, text='Quit', command=self.quit)
		self.quitButton.grid(row=0, column=0)
		self.quitButton.grid(row=1, column=0)
		self.quitButton2.grid(row=0, column=1)

	def createMenu(self):
		self.menu




app = Application()
app2 = Application2()

app.master.title('Sample application')
app.mainloop()

app2.master.title('Sample application')
app2.mainloop()
