
import pandas as pd

import math


	# options to print full array output
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

#the notes of the fretboard represented in a matrix
fretboard=[["E4","F4","F#4","G4","G#4","A4","A#4","B4","C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5","C6", "C#6", "D6", "D#6", "E6"],
["B3","C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4","A#4","B4","C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5"],
["G3", "G#3", "A3", "A#3", "B3","C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4","A#4","B4","C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5"],
["D3", "D#3", "E3", "F3", "F#3","G3", "G#3", "A3", "A#3", "B3","C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4","A#4","B4","C5", "C#5", "D5"],
["A2", "A#2", "B2","C3", "C#3","D3", "D#3", "E3", "F3", "F#3","G3", "G#3", "A3", "A#3", "B3","C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4"],
["E2", "F2", "F#2","G2", "G#2", "A2", "A#2", "B2","C3", "C#3","D3", "D#3", "E3", "F3", "F#3","G3", "G#3", "A3", "A#3", "B3","C4","C#4","D4","D#4","E4"]]
def run(csvFile):
	#an algorithm that recieves a frequency and returns the musical note affiliated (string)
	def pitch(freq):
		A4 = 440
		C0 = A4*pow(2, -4.75)
		name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
		h = round(12*math.log((freq/C0),2))
		h=int(h)
		octave = h // 12
		n = h % 12
		return name[n] +str(octave)

	#reads the frequency for every reading and calls pitch to get note returns the array of notes
	def findPitches():
		pitches=[]
		for i in goodReadings['frequency']:
			pitches.append(pitch(i))
		return pitches

	#returns an array of the location on the fretboard of all the occurences of a given note
	def findFretboardOccurences(Note):
		occurences=[]
		for i in range(6):
			for j in range(25):
				if fretboard[i][j]==Note:
					occurences.append((i,j))
		return occurences

	#returns the closest locattion of a given note by figuring out which occurence of the note is closest to the second to last note played
	def closestNote(two,one, Note):
		noteArray=findFretboardOccurences(Note)
		if two is None and one is None:
			if len(noteArray)==0:
				print ("NOTE NOT AVAILABLE ON STANDARD FRETBOARD: " + Note)
				return None
			return noteArray[version%len(noteArray)]
		elif two is None:
			two=one
		minDist =None
		tabWithMin=None
		for i in noteArray:
			if minDist is None:
				minDist=abs(i[0]-two[0])+abs(i[1]-two[1])
				tabWithMin=i
			else:
				dist=abs(i[0]-two[0])+abs(i[1]-two[1])
				if dist <=minDist:
					minDist=dist
					tabWithMin=i
		return tabWithMin

	#finds the most efficient location on the fretboard to play the notes 

	def findTabs():
		tabs=[]
		prevTab=None
		b4prevTab=None
		currentTab=None
		prevNote=None
		for i in goodReadings['Note']:
			if(i == prevNote):
				tabs.append(currentTab)
			else:
				currentTab=closestNote(b4prevTab,prevTab,i)
				if currentTab != None:
					tabs.append(currentTab)
					b4prevTab=prevTab
					prevTab=currentTab
					prevNote=i
				else:
					tabs.append("nan")
			
		return tabs

	def display():
		print ("e B G D A E")
		for i in goodReadings['Tab']:
			 
			for string in range(6):
				if string==i[0]:
					print(i[1]) ,
				else:
					print ("|"),
			print
	def truncate():
		return goodReadings.loc[goodReadings['Note'].shift()!=goodReadings['Note']]

	goodReadings=pd.read_csv(csvFile)

	#only uses readings with a cood qualtiy
	goodReadings=goodReadings[goodReadings['confidence']>0.6]
	pitches=findPitches()
	goodReadings['Note']=pitches

	#the nature of the fretboard allows for many different ways to play a riff, this section displays a few of those
	version=0
	next="next"
	while next=="next" or next=="Next":
		tabs=findTabs()
		goodReadings['Tab']=tabs
		goodReadings=truncate()
		print(goodReadings)
		display()
		next=input("Type next for another tablature: ")
		version+=1







