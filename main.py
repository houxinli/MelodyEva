from au import SimpleRecorder
from au.pitch_analyzer import PitchAnalyzer
from beat_ import Tempo
import threading
import numpy as np
import time
import eel

print ("pa_test.py __name__ :", __name__)

@eel.expose
def stopRecorder():
	print("stopRecorder")
	global SR
	SR.stop()
	SR.join()

@eel.expose
def initRecorder():
	global SR
	SR.start()
	print("initRecorder")
	# sec = 0
	# while sec < 15:
	# 	score_pitch = PA.getScore()
	# 	print("sec: ", sec)
	# 	print("score_pitch:", score_pitch)
	# 	time.sleep(1)
	# 	sec += 1
	# stopRecorder()

@eel.expose
def getScore():
	global PA
	score_pitch = PA.getScore()
	score_beat = getBeatScore()
	print("score_pitch : ", score_pitch )
	return score_pitch * 100, score_beat
	# return score_pitch

def getBeatScore():
	global PA, BA
	y1 = np.array(PA.original[PA.cpos:PA.cpos + PA.refresh_size]).astype(np.float32)
	y2 = np.array(PA.audio_data[PA.cpos:PA.cpos + PA.refresh_size]).astype(np.float32)
	score_beat = BA.beatevaluation(y1, y2, PA.sr)
	return score_beat

if __name__ == '__main__':

	eel.init('web')                     # Give folder containing web files

	# 创建录音机
	SR = SimpleRecorder()

	# 创建分析器
	PA = PitchAnalyzer(refresh_time = 10)
	BA = Tempo()

	# 注册分析器
	SR.register(PA)


	eel.start('index.html', size=(1536, 864))    # Start
# eel.start('realtime.html', size=(1536, 864))    # Start
