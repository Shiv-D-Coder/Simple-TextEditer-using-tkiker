import tkinter
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

class Notepad:

	# Initialize the tkinter root window
	__root = Tk()

	# Default window width and height
	__thisWidth = 300
	__thisHeight = 300

	# Text area to display and edit the text
	__thisTextArea = Text(__root)

	# Menu bar and its menus
	__thisMenuBar = Menu(__root)
	__thisFileMenu = Menu(__thisMenuBar, tearoff=0)
	__thisEditMenu = Menu(__thisMenuBar, tearoff=0)
	__thisHelpMenu = Menu(__thisMenuBar, tearoff=0)
	
	# Scrollbar for the text area
	__thisScrollBar = Scrollbar(__thisTextArea)	
	__file = None

	def __init__(self, **kwargs):

		# Set icon for the Notepad window
		try:
			self.__root.wm_iconbitmap("Notepad.ico")
		except:
			pass

		# Set window size (the default is 300x300)
		try:
			self.__thisWidth = kwargs['width']
		except KeyError:
			pass

		try:
			self.__thisHeight = kwargs['height']
		except KeyError:
			pass

		# Set the window title
		self.__root.title("Untitled - Notepad")

		# Center the window on the screen
		screenWidth = self.__root.winfo_screenwidth()
		screenHeight = self.__root.winfo_screenheight()
		left = (screenWidth / 2) - (self.__thisWidth / 2)
		top = (screenHeight / 2) - (self.__thisHeight / 2)
		self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth,
											self.__thisHeight,
											left, top))

		# Make the textarea auto resizable
		self.__root.grid_rowconfigure(0, weight=1)
		self.__root.grid_columnconfigure(0, weight=1)

		# Add controls (widgets) to the window
		self.__thisTextArea.grid(sticky=N + E + S + W)

		# Menu options for File menu
		self.__thisFileMenu.add_command(label="New", command=self.__newFile)
		self.__thisFileMenu.add_command(label="Open", command=self.__openFile)
		self.__thisFileMenu.add_command(label="Save", command=self.__saveFile)
		self.__thisFileMenu.add_separator()
		self.__thisFileMenu.add_command(label="Exit", command=self.__quitApplication)
		self.__thisMenuBar.add_cascade(label="File", menu=self.__thisFileMenu)	

		# Menu options for Edit menu
		self.__thisEditMenu.add_command(label="Cut", command=self.__cut)
		self.__thisEditMenu.add_command(label="Copy", command=self.__copy)
		self.__thisEditMenu.add_command(label="Paste", command=self.__paste)
		self.__thisMenuBar.add_cascade(label="Edit", menu=self.__thisEditMenu)	

		# Menu options for Help menu
		self.__thisHelpMenu.add_command(label="About Notepad", command=self.__showAbout)
		self.__thisMenuBar.add_cascade(label="Help", menu=self.__thisHelpMenu)

		# Attach the menu bar to the root window
		self.__root.config(menu=self.__thisMenuBar)

		# Attach a scrollbar to the text area
		self.__thisScrollBar.pack(side=RIGHT, fill=Y)				
		self.__thisScrollBar.config(command=self.__thisTextArea.yview)
		self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)
	
		
	def __quitApplication(self):
		# Destroy the root window and exit the application
		self.__root.destroy()

	def __showAbout(self):
		# Display information about the Notepad (About dialog)
		showinfo("Notepad", "Mrinal Verma")

	def __openFile(self):
		# Open an existing file and display its content in the text area
		self.__file = askopenfilename(defaultextension=".txt",
									filetypes=[("All Files", "*.*"),
												("Text Documents", "*.txt")])

		if self.__file == "":
			# No file selected or canceled
			self.__file = None
		else:
			# Try to open the file and display its content
			self.__root.title(os.path.basename(self.__file) + " - Notepad")
			self.__thisTextArea.delete(1.0, END)
			with open(self.__file, "r") as file:
				self.__thisTextArea.insert(1.0, file.read())

	def __newFile(self):
		# Create a new blank file in the text editor
		self.__root.title("Untitled - Notepad")
		self.__file = None
		self.__thisTextArea.delete(1.0, END)

	def __saveFile(self):
		if self.__file is None:
			# Save as a new file
			self.__file = asksaveasfilename(initialfile='Untitled.txt',
											defaultextension=".txt",
											filetypes=[("All Files", "*.*"),
														("Text Documents", "*.txt")])

			if self.__file == "":
				self.__file = None
			else:
				# Try to save the file
				with open(self.__file, "w") as file:
					file.write(self.__thisTextArea.get(1.0, END))
				self.__root.title(os.path.basename(self.__file) + " - Notepad")
		else:
			# Save the existing file
			with open(self.__file, "w") as file:
				file.write(self.__thisTextArea.get(1.0, END))

	def __cut(self):
		# Cut selected text in the text area
		self.__thisTextArea.event_generate("<<Cut>>")

	def __copy(self):
		# Copy selected text in the text area
		self.__thisTextArea.event_generate("<<Copy>>")

	def __paste(self):
		# Paste text from the clipboard into the text area
		self.__thisTextArea.event_generate("<<Paste>>")

	def run(self):
		# Run the main application
		self.__root.mainloop()

# Run main application
notepad = Notepad(width=600, height=400)
notepad.run()
