# Libraries imported: tkinter for gui, youtube_dl to download songs, urllib.request for checking internet connection
from tkinter import *
import youtube_dl
import urllib.request
import os

# Global vars
mainWindow = Tk() #for tkinter window
userInput = StringVar() #to trace the user's input
upperFrame = Frame(mainWindow) #for the youtube gui
errorFrame  = Frame(mainWindow) #for no internet prompt
# songDownloadedFrame = Frame(man)

# To hide the upper frame so that error frame can be shown
def hide(frame):
	print("HIDDEN")
	frame.grid_forget()

# To hide the error frame so that upper frame can be shown
def backToGui(frame):
	frame.grid_forget()
	connection = True
	gui(connection)

def prompt(frame, txt):
	frame.grid()
	backButton = Button(frame, text = "Go Back", fg = "blue")
	backButton.bind("<Button-1>", lambda x: backToGui(frame))
	errorPrompt = Label(frame, text = txt, fg = "red")
	backButton.grid(row = 0, column = 1)
	errorPrompt.grid(row = 0, column = 2)

# To display the gui
def gui(connection):
	if connection:
		upperFrame.grid()
		name = Label(upperFrame, text = "Enter the song")
		usrName = Entry(upperFrame, textvariable = userInput)
		usrName.delete("0", END)
		usrName.insert(0, "")
		usrName.bind("<Return>", lambda x: dowloadVid())
		name.grid(row=0, column=0, sticky = W)
		usrName.grid(row=0, column=1)
		button1 = Button(upperFrame, text = "Enter", fg = "red")
		button1.bind("<Button-1>", lambda x: dowloadVid())
		button1.grid(row=0, column = 2)
	else:
		hide(upperFrame)
		prompt(errorFrame, "NO INTERNET CONNECTION")
		# errorFrame.grid()
		# backButton = Button(errorFrame, text = "Go Back", fg = "blue")
		# backButton.bind("<Button-1>", lambda x: backToGui(errorFrame))
		# errorPrompt = Label(errorFrame, text = "NO INTERNET CONNECTION", fg = "red")
		# backButton.grid(row = 0, column = 1)
		# errorPrompt.grid(row = 0, column = 2)

# Checking for internet connection
def internetConnection():
	req = urllib.request.Request("https://www.youtube.com/")
	try:
		urllib.request.urlopen(req)
		return True
	except urllib.error.URLError as e:
		print("NO INTERNET MOTHERFUCKER")
		return False

# Checking for valid string input
def validation(link):
	if ("https://www.youtube.com/watch?v=" in link) and (len(link[32:]) == 11):
		return True
	return False

# To edit the string if the link is from a playlist
def editString(link):
	if "&list" in link:
		link = link[:43]
		return link
	return link

def songDownloaded(frame):
	hide(upperFrame)
	prompt(errorFrame, "SONG DOWNLOADED")

def songNotDownloaded(frame):
	hide(upperFrame)
	prompt(errorFrame, "SONG NOT DOWNLOADED")

def downloaded(vID):
	extention = vID + ".mp3"
	songs = os.listdir()
	found = False
	counter = 0
	while not found:
		if extention in songs[counter]:
			found = True
		counter+=1
	if found:
		songDownloaded(upperFrame)
	else:
		songNotDownloaded(upperFrame)


# Downloading the song
def dowloadVid():
	connection = internetConnection()
	print(connection)
	ydl_options = {
		'format': 'bestaudio/best',
		'postprocessors': [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
		'preferredquality': '192',
		}]
	}	
	if(connection):
		link = userInput.get()
		song = editString(link)
		valid = validation(song)
		vID = song[32:]
		if valid:
			with youtube_dl.YoutubeDL(ydl_options) as ydl:
				ydl.download([song])
			print("song downloaded")		
			vID = song[32:]
			downloaded(vID)
	else:
		gui(connection)

def main():
	connection = True
	gui(connection)
	# downloaded(vID)

main()
mainWindow.mainloop()
