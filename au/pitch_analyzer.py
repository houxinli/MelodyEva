from .base_analyzer import BaseAnalyzer
import librosa
import time
import math
import numpy as np

print ("pitch_analyzer __name__ :", __name__)

class PitchAnalyzer(BaseAnalyzer):
    def __init__(self,
            refresh_time = 1
            ):
        BaseAnalyzer.__init__(self)
        self.refresh_time = refresh_time
        self.cpos = 0
        self.result = []
        self.counter = 0

    def register_recorder(self,recorder):
        BaseAnalyzer.register_recorder(self,recorder)
        self.refresh_size = self.sr * self.refresh_time

    def data_process(self,data):
        self.counter += 1
        return self.counter

    def getScore(self):
        return self.counter

    def run(self):
        while self.recorder.start_time is None:
            time.sleep(1)

        while self.running.isSet():
            while len(self.audio_data) > self.cpos + self.refresh_size:
                data = np.array(self.audio_data[self.cpos:self.cpos + self.refresh_size]).astype(np.float32)
                data = self.data_process(data)
                self.result.append(data)
                self.cpos += self.refresh_size