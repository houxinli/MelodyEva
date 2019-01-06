import numpy as np
import librosa
import matplotlib.pyplot as plt
import librosa.display
from dtw import dtw
import math

class Tempo:

    def __init__(self):
        return

    def beat_track(self,y,sr):
        localscore, period, tightness=self.onsetdetection(y, sr)
        return self.beattrack_dp(localscore, period, tightness)

    def beatevaluation(self,y1,y2,sr):
        samplebeats = self.beat_track(y=y1, sr=sr)
        diff_samplebeats = librosa.feature.delta(samplebeats)
        audiobeats = self.beat_track(y=y2, sr=sr)
        diff_audiobeats = librosa.feature.delta(audiobeats)
        dist, cost, acc, path = dtw(diff_samplebeats.reshape(-1, 1), diff_audiobeats.reshape(-1, 1),
                                    dist=lambda x, y: np.linalg.norm(x - y, ord=1))
        mark = (max(0,(1 - math.atan(dist / 10)))) * 100  # 10是上线
        return mark

    def beattrack_dp(self,localscore,period,tightness):
        beats=[]
        backlink=np.zeros(localscore.shape)
        cumscore = np.zeros(localscore.shape)
        periodrange=np.arange(-2*period,-int(period/2)+1,dtype=int)
        #skewed window
        txwt=-tightness*(np.log(-periodrange/period)**2)
        flag=1
        for i,score in enumerate(localscore):
            timerange=i+periodrange
            zpad=int(max(0,min(-timerange[0],len(timerange))))
            candidate=txwt.copy()
            candidate[zpad:]=candidate[zpad:]+cumscore[timerange[zpad:]]
            maxbeatpos=np.argmax(candidate)
            cumscore[i]=score+candidate[maxbeatpos]
            if flag==1 and localscore[i]<0.01*max(localscore):
                backlink[i]=-1
            else:
                backlink[i]=timerange[maxbeatpos]
                flag=0
        print(backlink)
        print(cumscore)
        maxindex=np.where(cumscore == np.max(cumscore))
        medscore=np.median(cumscore[maxindex])
        bestendpos=cumscore*medscore>0.5*medscore
        end=np.argwhere(bestendpos).max()
        print(end)
        beats.append(int(end))
        while backlink[beats[-1]]>=0:
            beats.append(int(backlink[beats[-1]]))
        beats.reverse()
        print(beats)
        print(len(beats))
        return beats

    def onsetdetection(self,y,sr):
        print(y.shape)
        sro=22050
        swin=2048 #window size
        shop=512
        step=swin/shop
        oesr=sro/shop #the sampel rate for  the specgram frames
        if sro!=sr:
            y=librosa.resample(y, sr, sro)
        D=np.abs(librosa.stft(y, n_fft=2048, hop_length=shop, win_length=swin, window='hann',
             center=True, dtype=np.complex64, pad_mode='reflect'))
        amp_db = librosa.power_to_db(D,ref=1.0, amin=1e-10, top_db=80.0)
        lag=1
        diff = np.maximum(amp_db[:, :-lag] - amp_db[:, lag:], 0.0)
        mean_onset=np.mean(diff,axis=0) #raw onset decision waveform
        #calculate the throshold
        sum=0
        nozero=[]
        count=0
        for i in mean_onset:
            if i!=0:
                sum+= i
                nozero.append(i)
                count+=1
        meanofsum=sum/count
        tmplist=list((np.array(nozero)-meanofsum)**2)
        stadvar=np.sqrt(1/count*np.sum(tmplist))
        onset = mean_onset
        for i in range(len(onset)):
            if onset[i]<meanofsum:
                onset[i] = 0
        #This is tempo estimate...maybe not so accurate
        bpm = librosa.beat.tempo(onset_envelope=onset, sr=sr,hop_length = shop)[0]
        #oesr
        period=round(60*oesr/bpm)
        #AGC on onset
        onset = onset / np.std(onset,ddof=1)
        #smooth beat events
        window=np.exp(-0.5*(np.arange(-period,period+1)/period*32)**2)
        localscore=np.convolve(onset,window,'same')
        tightness=100
        return localscore,period,tightness


"""
#tempogram = librosa.feature.tempogram(onset_envelope=onset, sr=sr,hop_length = shop)
#print(tempogram)
start_bpm = 120
std = 1.0
automaxsize=round(4*oesr) #4s
ac_global = librosa.autocorrelate(onset, automaxsize)
ac_local=ac_global[automaxsize:automaxsize*2]
bpms=60*oesr/np.arange(0.1,automaxsize+0.1)
ac_window=np.exp(-0.5*((np.log2(bpms/start_bpm))/std)**2)
bestperiodindex = np.argmax(ac_local* ac_window)
if bestperiodindex==0:
    bestperiod=start_bpm
else:
    bestperiod=

"""

