
from recorder import Recorder
from datetime import datetime
def buildIt ():
	rec=Recorder(channels=2)
	poop=rec.open('./savedRecordings/'+datetime.now().strftime("%d_%m_%Y_%H_%M_%S")+".wav", 'wb')
	poop.start_recording()
	return poop
def cutItOut(poop):
	print("STOOPING RECORDING")
	poop.stop_recording()

