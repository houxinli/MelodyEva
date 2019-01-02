from au import SimpleRecorder
from au.pitch_analyzer import PitchAnalyzer
import time
import eel

print ("pa_test.py __name__ :", __name__)
if __name__ == '__main__':

	eel.init('web')                     # Give folder containing web files

	# 创建录音机
	SR = SimpleRecorder()

	# 创建分析器
	PA = PitchAnalyzer(refresh_time = 1)

	# 注册分析器
	SR.register(PA)

@eel.expose
def initRecorder():
	global SR
	SR.start()

@eel.expose
def stopRecorder():
	global SR
	SR.stop()
	SR.join()



	eel.start('index.html', size=(1536, 864))    # Start
