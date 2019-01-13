from .base_analyzer import BaseAnalyzer
import time
import math
import numpy as np, scipy, matplotlib.pyplot as plt
import librosa, librosa.display


#print ("pitch_analyzer __name__ :", __name__)
# acf and deal with voice
def deal1_pa(x, sr):
    # x, sr = librosa.load(path)  # read the voice
    # sr = self.sr
    f_hi = 1100  # the highest voice of women
    f_lo = 82  # the lowest voice of man
    t_lo = sr / f_hi  # the possible shortest time of the highest peak appear
    t_hi = sr / f_lo  # the possible longest time of the highest peak appear
    max0 = int((len(x) - 440) / 220) - 1  # duration=max*20ms
    h0 = np.empty([max0, ], dtype=float)
    # calculate the frequency in each 20ms
    for i in range(0, max0):
        r = librosa.autocorrelate(x[(i * 220):(440 + i * 220)])
        r[:int(t_lo)] = 0
        r[int(t_hi):] = 0
        t_max = r.argmax()
        if (t_max > t_lo and t_max <= t_hi):
            h0[i] = float(sr) / t_max
        else:
            h0[i] = 0

            # data processing
            # minus the empty time in the front of frequency array and at last of array
    for i in range(0, max0):
        if h0[i] != 0:
            h0 = h0[i:]
            max0 = max0 - i
            break
    for i in range(0, max0):
        if h0[max0 - i - 1] != 0:
            h0 = h0[:(max0 - i)]
            max0 = max0 - i
            break

            # step 1:Smooth processing
    temp = np.empty([5, ], dtype=int)
    for i in range(0, max0 - 6):
        for j in range(0, 5):
            temp[j] = h0[i + j]
        for j in range(0, 5):
            for k in range(j + 1, 5):
                if temp[j] < temp[k]:
                    t = temp[k]
                    temp[k] = temp[j]
                    temp[j] = t
        for j in range(0, 5):
            if h0[i + j] == temp[2]:
                t = h0[i + j]
                h0[i + j] = h0[i + 2]
                h0[i + 2] = t

                # step2:calculate mean value
    for i in range(0, int(max0 / 5 - 1)):
        flag = 1
        average_all = 0
        for j in range(0, 5):
            average_all += h0[i * 5 + j]
            if h0[i * 5 + j] == 0:
                flag = 0
        if flag == 1:
            average = average_all / 5
            for j in range(0, 5):
                h0[i * 5 + j] = average

                # step3:resolve the value of zero
    for i in range(0, max0):
        if h0[i] < 80:
            h0[i] = 0

            # step4: remove the motation value
    for i in range(1, max0 - 1):
        if h0[i - 1] == 0 and h0[i + 1] == 0:
            h0[i] = 0

    # translate pitch into midi note
    n0 = np.empty([max0, ], dtype=float)
    for i in range(0, max0):
        if h0[i] > 80:
            n0[i] = float(librosa.hz_to_midi(h0[i]))
        else:
            n0[i] = -1
    # minus the zero in the front fo and the the last of the array
    for i in range(0, len(n0)):
        if n0[i] != 0:
            n0 = n0[i:]
            break
    for i in range(0, len(n0)):
        if n0[len(n0) - 1 - i] != 0:
            n0 = n0[:(len(n0) - i)]
            break
    return (n0)
def deal1_da(data):
    sr = 22050
    f_hi = 1100  # the highest voice of women
    f_lo = 82  # the lowest voice of man
    t_lo = sr / f_hi  # the possible shortest time of the highest peak appear
    t_hi = sr / f_lo  # the possible longest time of the highest peak appear
    max0 = int((len(data) - 440) / 220) - 1  # duration=max*20ms
    h0 = np.empty([max0, ], dtype=float)
    # calculate the frequency in each 20ms
    for i in range(0, max0):
        r = librosa.autocorrelate(data[(i * 220):(440 + i * 220)])
        r[:int(t_lo)] = 0
        r[int(t_hi):] = 0
        t_max = r.argmax()
        if (t_max > t_lo and t_max <= t_hi):
            h0[i] = float(sr) / t_max
        else:
            h0[i] = 0

            # data processing
            # minus the empty time in the front of frequency array and at last of array
    for i in range(0, max0):
        if h0[i] != 0:
            h0 = h0[i:]
            max0 = max0 - i
            break
    for i in range(0, max0):
        if h0[max0 - i - 1] != 0:
            h0 = h0[:(max0 - i)]
            max0 = max0 - i
            break

            # step 1:Smooth processing
    temp = np.empty([5, ], dtype=int)
    for i in range(0, max0 - 6):
        for j in range(0, 5):
            temp[j] = h0[i + j]
        for j in range(0, 5):
            for k in range(j + 1, 5):
                if temp[j] < temp[k]:
                    t = temp[k]
                    temp[k] = temp[j]
                    temp[j] = t
        for j in range(0, 5):
            if h0[i + j] == temp[2]:
                t = h0[i + j]
                h0[i + j] = h0[i + 2]
                h0[i + 2] = t

                # step2:calculate mean value
    for i in range(0, int(max0 / 5 - 1)):
        flag = 1
        average_all = 0
        for j in range(0, 5):
            average_all += h0[i * 5 + j]
            if h0[i * 5 + j] == 0:
                flag = 0
        if flag == 1:
            average = average_all / 5
            for j in range(0, 5):
                h0[i * 5 + j] = average

                # step3:resolve the value of zero
    for i in range(0, max0):
        if h0[i] < 80:
            h0[i] = 0

            # step4: remove the motation value
    for i in range(1, max0 - 1):
        if h0[i - 1] == 0 and h0[i + 1] == 0:
            h0[i] = 0

    # translate pitch into midi note
    n0 = np.empty([max0, ], dtype=float)
    for i in range(0, max0):
        if h0[i] > 80:
            n0[i] = float(librosa.hz_to_midi(h0[i]))
        else:
            n0[i] = -1

    # minus the zero in the front fo and the the last of the array
    for i in range(0, len(n0)):
        if n0[i] != 0:
            n0 = n0[i:]
            break
    for i in range(0, len(n0)):
        if n0[len(n0) - 1 - i] != 0:
            n0 = n0[:(len(n0) - i)]
            break
    return (n0)
def Z_ScoreNormalization(x,mu,sigma):
    for i in range(0,12):
        x[i] = (x[i] - mu) / sigma
    return x
def deal2_pa(path):
    x, sr = librosa.load(path)  # read the voice

    chroma = librosa.feature.chroma_stft(y=x, sr=sr)
    chroma = np.transpose(chroma)
    for i in range(0,len(chroma)):
        chroma[i] = Z_ScoreNormalization(chroma[i], np.average(chroma[0]), np.std(chroma[0]))
    return chroma
def deal2_da(data):
    chroma = librosa.feature.chroma_stft(y=data, sr=22050)
    chroma = np.transpose(chroma)
    for i in range(0,len(chroma)):
        chroma[i] = Z_ScoreNormalization(chroma[i], np.average(chroma[0]), np.std(chroma[0]))
    return chroma

class PitchAnalyzer(BaseAnalyzer):
    def __init__(self,
            refresh_time = 1,
            path = "mp3/source_2.mp3"
            ):
        BaseAnalyzer.__init__(self)
        self.refresh_time = refresh_time
        self.cpos = 0
        self.result = []
        self.counter = 0
        self.original, self.sr = librosa.load(path)

    def register_recorder(self,recorder):
        BaseAnalyzer.register_recorder(self,recorder)
        self.refresh_size = self.sr * self.refresh_time

    def data_process(self,data):
        nt0 = deal1_pa(data, self.sr)
        nt1 = deal1_da(data)
        #print(nt0)
        #print(nt1)
        # choose the shortest voice

        scale = float(len(nt1)) / len(nt0)
        #print(scale)
        # compare with the Pitch standards
        # relatively
        compare = 0.0
        count1 = 0
        delta = 0.0
        for i in range(0, len(nt0)):
            if nt0[i] > 0 and i * scale < len(nt1) and nt1[int(i * scale)] > 0:
                delta += nt0[i] - nt1[int(i * scale)]
                count1 += 1
        delta = delta / count1
        for i in range(0, len(nt0)):
            if nt0[i] > 0 and i * scale < len(nt1) and nt1[int(i * scale)] > 0:
                compare += float(abs(nt0[i] - nt1[int(i * scale)] - delta)) / 40
        pitch_mark1 = 1 - compare / count1
        #print ("pitch_mark1:")
        #print (pitch_mark1*0.1)

        chroma0 = deal2_pa("mp3/source_2.mp3")
        chroma1 = deal2_da(data)
        chroma0 = np.transpose(chroma0)
        chroma1 = np.transpose(chroma1)
        cost = 0
        D, wp = librosa.sequence.dtw(chroma0, chroma1, subseq=True)
        for i in range(0,len(chroma1[0])):
            cost += D[wp[i][1],wp[i][0]]
        pitch_mark2 = 1 - math.atan(cost/20) * 2 / math.pi
        #print ("pitch_mark2:")
        #print (pitch_mark2*0.9)
        #print ("pitch_mark:")

        self.counter = 0.1*pitch_mark1+0.9*pitch_mark2
        #print (self.counter)
        # self.counter = pitch_mark2
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