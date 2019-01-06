from au import SimpleRecorder
from au.pitch_analyzer import PitchAnalyzer
import threading
import time
import eel

print ("pa_test.py __name__ :", __name__)

@eel.expose
def stopRecorder():
	global SR
	SR.stop()
	SR.join()

@eel.expose
def initRecorder():
	global SR
	SR.start()
	sec = 0
	while sec < 15:
		score_pitch = PA.getScore()
		print("sec: ", sec)
		print("score_pitch:", score_pitch)
		time.sleep(1)
		sec += 1
	stopRecorder()


if __name__ == '__main__':

	eel.init('web')                     # Give folder containing web files

	# 创建录音机
	SR = SimpleRecorder()

	# 创建分析器
	PA = PitchAnalyzer(refresh_time = 1)

	# 注册分析器
	SR.register(PA)


	eel.start('index.html', size=(1536, 864))    # Start
# eel.start('realtime.html', size=(1536, 864))    # Start
