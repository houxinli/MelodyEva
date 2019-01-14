from au import SimpleRecorder, VolumeAnalyzer
from au.pitch_analyzer import PitchAnalyzer
import time

print ("pa_test.py __name__ :", __name__)
if __name__ == '__main__':


	# 创建录音机
	SR = SimpleRecorder()

	# 创建分析器
	PA = PitchAnalyzer(refresh_time = 1)
	VA = VolumeAnalyzer(rec_time = 1)

	# 注册分析器
	SR.register(PA)
	SR.register(VA)

	SR.start()

	sec = 0
	while sec < 15:
		# score_pitch = PA.getScore()
		volume = VA.get_volume ()
		print("sec: ", sec, "volume: ", volume)
		# print("score_pitch:", score_pitch)
		time.sleep(1)
		sec += 1

	SR.stop()
	SR.join()

	print('end')
