import numpy as np
import pandas as pd
import librosa
from audioread import NoBackendError
from sklearn.neighbors import KNeighborsClassifier


# 识别的时间在10s左右
class MusicEmotionRecognizer:
    def __init__(self, featureFile='MER/EmotionFeatures2.csv'):
        """
        初始化情绪识别类
        :param featureFile: 特征文件，默认是同级目录下的'EmotionFeatures2.csv'文件
        """
        self.kNN = KNeighborsClassifier(n_neighbors=2)
        self.denos = []     # 归一化分母
        self.moles = []     # 归一化分子
        self._initClassifier(featureFile)

    def _initClassifier(self, featureFile):
        data = pd.read_csv(featureFile)
        feature = data.loc[:, 'tempo':]     # 从'tempo'列开始到最后的所有行
        featureName = list(feature)         # 所有“列索引值”的列表
        # 特征归一化
        for name in featureName:
            deno = feature[name].max()
            mole = feature[name].min()
            self.denos.append(deno - mole)
            self.moles.append(mole)
            feature[name] = (feature[name] - mole) / (deno - mole)

        features = feature.values               # 抽象成二维矩阵
        labels = data.loc[:, 'label'].dropna()  # 情绪标签
        # print(labels)
        self.kNN.fit(features, labels)

    def predictEmotion(self, songFile):
        """
        识别情绪
        :param songFile: 音频文件（大于2min）
        :return: 情绪类别数字
        1-sad, 2-happy, 3-relax, 4-angry
        """
        feature_set = self._extractFeature(songFile)
        feature = feature_set.loc[:, 'tempo':]
        featureName = list(feature)      # 所有“列索引值”的列表
        # 特征归一化
        for i in range(1, len(featureName)):
            name = featureName[i]
            feature[name] = (feature[name] - self.moles[i]) / self.denos[i]
        res = self.kNN.predict(feature)
        clas = {"sad": 1, "happy": 2, "relax": 3, "angry": 4}
        # return clas[res[0]]
        return res[0]

    def _extractFeature(self, file):
        feature_set = pd.DataFrame()  # 特征矩阵

        # 单独的特征向量
        tempo_vector = pd.Series()
        total_beats = pd.Series()
        average_beats = pd.Series()
        chroma_stft_mean = pd.Series()
        chroma_stft_var = pd.Series()
        mel_mean = pd.Series()
        mel_var = pd.Series()
        mfcc_mean = pd.Series()
        mfcc_var = pd.Series()
        mfcc_delta_mean = pd.Series()
        mfcc_delta_var = pd.Series()
        rmse_mean = pd.Series()
        rmse_var = pd.Series()
        cent_mean = pd.Series()
        cent_var = pd.Series()
        spec_bw_mean = pd.Series()
        spec_bw_var = pd.Series()
        contrast_mean = pd.Series()
        contrast_var = pd.Series()
        rolloff_mean = pd.Series()
        rolloff_var = pd.Series()
        poly_mean = pd.Series()
        poly_var = pd.Series()
        tonnetz_mean = pd.Series()
        tonnetz_var = pd.Series()
        zcr_mean = pd.Series()
        zcr_var = pd.Series()
        harm_mean = pd.Series()
        harm_var = pd.Series()
        perc_mean = pd.Series()
        perc_var = pd.Series()
        frame_mean = pd.Series()
        frame_var = pd.Series()

        # 取前60秒
        try:
            y, sr = librosa.load(file, sr=22050, offset=0, duration=60)
        except NoBackendError:
            print("File Error.")
            return
        print(y.shape)
        S = np.abs(librosa.stft(y))

        # 提取特征
        tempo, beats = librosa.beat.beat_track(y, sr)
        # print(tempo, beats)
        chroma_stft = librosa.feature.chroma_stft(y, sr)
        melspectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
        rmse = librosa.feature.rmse(y=y)
        cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        contrast = librosa.feature.spectral_contrast(S=S, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        poly_features = librosa.feature.poly_features(S=S, sr=sr)
        tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        harmonic = librosa.effects.harmonic(y)
        percussive = librosa.effects.percussive(y)

        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        mfcc_delta = librosa.feature.delta(mfcc)

        onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
        frames_to_time = librosa.frames_to_time(onset_frames[:20], sr=sr)

        id = 0
        # 转换特征
        tempo_vector.at[id] = tempo  # tempo
        total_beats.at[id] = sum(beats)  # beats 节奏
        average_beats.at[id] = np.average(beats)
        chroma_stft_mean.at[id] = np.mean(chroma_stft)  # chroma stft STFT色度
        chroma_stft_var.at[id] = np.var(chroma_stft)
        mel_mean.at[id] = np.mean(melspectrogram)  # melspectrogram 梅尔频谱
        mel_var.at[id] = np.var(melspectrogram)
        mfcc_mean.at[id] = np.mean(mfcc)  # mfcc MFCC特征
        mfcc_var.at[id] = np.var(mfcc)
        mfcc_delta_mean.at[id] = np.mean(mfcc_delta)  # mfcc delta
        mfcc_delta_var.at[id] = np.var(mfcc_delta)
        rmse_mean.at[id] = np.mean(rmse)  # rmse
        rmse_var.at[id] = np.var(rmse)
        cent_mean.at[id] = np.mean(cent)  # cent
        cent_var.at[id] = np.var(cent)
        spec_bw_mean.at[id] = np.mean(spec_bw)  # spectral bandwidth
        spec_bw_var.at[id] = np.var(spec_bw)
        contrast_mean.at[id] = np.mean(contrast)  # contrast
        contrast_var.at[id] = np.var(contrast)
        rolloff_mean.at[id] = np.mean(rolloff)  # rolloff
        rolloff_var.at[id] = np.var(rolloff)
        poly_mean.at[id] = np.mean(poly_features)  # poly features
        poly_var.at[id] = np.var(poly_features)
        tonnetz_mean.at[id] = np.mean(tonnetz)  # tonnetz
        tonnetz_var.at[id] = np.var(tonnetz)
        zcr_mean.at[id] = np.mean(zcr)  # zero crossing rate
        zcr_var.at[id] = np.var(zcr)
        harm_mean.at[id] = np.mean(harmonic)  # harmonic
        harm_var.at[id] = np.var(harmonic)
        perc_mean.at[id] = np.mean(percussive)  # percussive
        perc_var.at[id] = np.var(percussive)
        frame_mean.at[id] = np.mean(frames_to_time)  # frames
        frame_var.at[id] = np.var(frames_to_time)

        # 合并所有特征并转换成csv, json文件
        feature_set['tempo'] = tempo_vector  # tempo
        feature_set['total_beats'] = total_beats  # beats
        feature_set['average_beats'] = average_beats
        feature_set['chroma_stft_mean'] = chroma_stft_mean  # chroma stft
        feature_set['chroma_stft_var'] = chroma_stft_var
        feature_set['melspectrogram_mean'] = mel_mean  # melspectrogram
        feature_set['melspectrogram_var'] = mel_var
        feature_set['mfcc_mean'] = mfcc_mean  # mfcc
        feature_set['mfcc_var'] = mfcc_var
        feature_set['mfcc_delta_mean'] = mfcc_delta_mean  # mfcc delta
        feature_set['mfcc_delta_var'] = mfcc_delta_var
        feature_set['rmse_mean'] = rmse_mean  # rmse
        feature_set['rmse_var'] = rmse_var
        feature_set['cent_mean'] = cent_mean  # cent
        feature_set['cent_var'] = cent_var
        feature_set['spec_bw_mean'] = spec_bw_mean  # spectral bandwidth
        feature_set['spec_bw_var'] = spec_bw_var
        feature_set['contrast_mean'] = contrast_mean  # contrast
        feature_set['contrast_var'] = contrast_var
        feature_set['rolloff_mean'] = rolloff_mean  # rolloff
        feature_set['rolloff_var'] = rolloff_var
        feature_set['poly_mean'] = poly_mean  # poly features
        feature_set['poly_var'] = poly_var
        feature_set['tonnetz_mean'] = tonnetz_mean  # tonnetz
        feature_set['tonnetz_var'] = tonnetz_var
        feature_set['zcr_mean'] = zcr_mean  # zero crossing rate
        feature_set['zcr_var'] = zcr_var
        feature_set['harm_mean'] = harm_mean  # harmonic
        feature_set['harm_var'] = harm_var
        feature_set['perc_mean'] = perc_mean  # percussive
        feature_set['perc_var'] = perc_var
        feature_set['frame_mean'] = frame_mean  # frames
        feature_set['frame_var'] = frame_var

        return feature_set


if __name__ == '__main__':
    er = MusicEmotionRecognizer()
    print(er.predictEmotion('逃.mp3'))
