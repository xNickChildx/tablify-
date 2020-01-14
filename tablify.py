import tkinter as T
import build
import wave 
import pyaudio
import os
import analyze
import crepe 
from scipy.io import wavfile

def record():
	def stopRec(recording):
			build.cutItOut(recording)
			stopBtn.pack_forget()

	recording=build.buildIt()
	stopBtn=T.Button(recFrame,text="Stop", command=lambda: stopRec(recording), bg="red", fg="white")
	try :
		stopBtn.pack()
	except NameError:
		stopBtn=T.Button(recFrame,text="Stop", command=lambda: stopRec(recording), bg="red", fg="white")


	file=[x for x in os.listdir("./savedRecordings") if x not in lb.get(0,lb.size())]
	
	
	for i in file:
		lb.insert(T.END, i)
	
		
def showTab():
	crepe.process_file("./savedRecordings/"+lb.get(lb.curselection()), output="csvFiles",viterbi=True)
	analyze.run("./csvFiles/"+lb.get(lb.curselection())[:-3]+"f0.csv")
	

def playRec():
	wf=wave.open("./savedRecordings/"+lb.get(lb.curselection()), 'rb')
	p=pyaudio.PyAudio()
	stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
	data=wf.readframes(1024)
	
	while len(data)>0:
		stream.write(data)
		data=wf.readframes(1024)
	
	stream.stop_stream()
	stream.close()
	p.terminate()
	return

	

bColor="#fbb"
fColor="#1a1"
master=T.Tk()
master.geometry("500x100")
#master.title("Tablify!")
frame=T.Frame(master, bg=bColor)
frame.pack(fill=T.BOTH,expand=1)

title=T.Label(frame, text="Welcome to Tablify", fg=fColor, bg=bColor)
title.pack(side=T.TOP)
recFrame=T.Frame(frame)
recFrame.pack()
lb=T.Listbox(frame)
btn=T.Button(recFrame,text="Record some yamss", command=record)
btn.pack(side=T.TOP)





files=os.listdir("./savedRecordings")

for i in range(len(files)):
	lb.insert(T.END,files[i])
playBtn=T.Button(frame, text="Play", fg="white", bg="green", command=playRec )
runBtn=T.Button(frame, text="Get Tab!", fg=fColor, bg=bColor, command=showTab )
lb.pack()
runBtn.pack()
playBtn.pack()
master.mainloop()

