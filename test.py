from MER.mer2 import MusicEmotionRecognizer
import time
from au import SimpleRecorder, VolumeAnalyzer

# 创建录音机
SR = SimpleRecorder()

# 创建分析器
# PA = PitchAnalyzer(rec_time = 1)
VA = VolumeAnalyzer(rec_time = 1)

# 注册分析器
# SR.register(PA)
SR.register(VA)

SR.start()

sec = 0
while sec < 15:
	Volume = VA.get_volume()
	# score_pitch = PA.getScore()
	print("sec: ", sec)
	# print("score_pitch:", score_pitch)
	print("Volume:", Volume)
	time.sleep(1)
	sec += 1

SR.stop()
SR.join()


er = MusicEmotionRecognizer()

clas1 = er.predictEmotion('web/record.wav')
# clas0 = er.predictEmotion('web/source_2.mp3')

print("clas1:", clas1)

