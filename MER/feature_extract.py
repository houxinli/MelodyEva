import librosa
import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join
from audioread import NoBackendError


def extract_features(path, label, emotionId, startid):
    """
    提取path目录下的音频文件的特征，使用librosa库
    :param path: 文件路径
    :param label: 情绪类型
    :param startid: 开始的序列号
    :return: 特征矩阵  pandas.DataFrame
    """
    id = startid    # 序列号
    feature_set = pd.DataFrame()   # 特征矩阵

    # 单独的特征向量
    labels = pd.Series()
    emotion_vector = pd.Series()
    songname_vector = pd.Series()
    tempo_vector = pd.Series()
    total_beats = pd.Series()
    average_beats = pd.Series()
    chroma_stft_mean = pd.Series()
    # chroma_stft_std = pd.Series()
    chroma_stft_var = pd.Series()
    # chroma_cq_mean = pd.Series()
    # chroma_cq_std = pd.Series()
    # chroma_cq_var = pd.Series()
    # chroma_cens_mean = pd.Series()
    # chroma_cens_std = pd.Series()
    # chroma_cens_var = pd.Series()
    mel_mean = pd.Series()
    # mel_std = pd.Series()
    mel_var = pd.Series()
    mfcc_mean = pd.Series()
    # mfcc_std = pd.Series()
    mfcc_var = pd.Series()
    mfcc_delta_mean = pd.Series()
    # mfcc_delta_std = pd.Series()
    mfcc_delta_var = pd.Series()
    rmse_mean = pd.Series()
    # rmse_std = pd.Series()
    rmse_var = pd.Series()
    cent_mean = pd.Series()
    # cent_std = pd.Series()
    cent_var = pd.Series()
    spec_bw_mean = pd.Series()
    # spec_bw_std = pd.Series()
    spec_bw_var = pd.Series()
    contrast_mean = pd.Series()
    # contrast_std = pd.Series()
    contrast_var = pd.Series()
    rolloff_mean = pd.Series()
    # rolloff_std = pd.Series()
    rolloff_var = pd.Series()
    poly_mean = pd.Series()
    # poly_std = pd.Series()
    poly_var = pd.Series()
    tonnetz_mean = pd.Series()
    # tonnetz_std = pd.Series()
    tonnetz_var = pd.Series()
    zcr_mean = pd.Series()
    # zcr_std = pd.Series()
    zcr_var = pd.Series()
    harm_mean = pd.Series()
    # harm_std = pd.Series()
    harm_var = pd.Series()
    perc_mean = pd.Series()
    # perc_std = pd.Series()
    perc_var = pd.Series()
    frame_mean = pd.Series()
    # frame_std = pd.Series()
    frame_var = pd.Series()

    # 遍历path中的所有音频文件
    file_data = [f for f in listdir(path) if isfile(join(path, f))]
    for line in file_data:
        if line[-1:] == '\n':
            # 最后一个字符是回车
            line = line[:-1]

        # 读取音频文件
        song = path + line
        print(song)
        # 取前60秒
        try:
            y, sr = librosa.load(song, sr=22050, offset=60, duration=60)
        except NoBackendError:
            continue
        S = np.abs(librosa.stft(y))

        # 提取特征
        tempo, beats = librosa.beat.beat_track(y, sr)
        chroma_stft = librosa.feature.chroma_stft(y, sr)
        # chroma_cq = librosa.feature.chroma_cqt(y, sr)
        # chroma_cens = librosa.feature.chroma_cens(y=y, sr=sr)
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

        # 转换特征
        labels.at[id] = label   # 标签（情绪）
        emotion_vector.at[id] = emotionId
        songname_vector.at[id] = line
        tempo_vector.at[id] = tempo  # tempo
        total_beats.at[id] = sum(beats)  # beats 节奏
        average_beats.at[id] = np.average(beats)
        chroma_stft_mean.at[id] = np.mean(chroma_stft)  # chroma stft STFT色度
        # chroma_stft_std.at[id] = np.std(chroma_stft)
        chroma_stft_var.at[id] = np.var(chroma_stft)
        # chroma_cq_mean.at[id] = np.mean(chroma_cq)  # chroma cq CQ色度
        # chroma_cq_std.at[id] = np.std(chroma_cq)
        # chroma_cq_var.at[id] = np.var(chroma_cq)
        # chroma_cens_mean.at[id] = np.mean(chroma_cens)  # chroma cens 中心色度
        # chroma_cens_std.at[id] = np.std(chroma_cens)
        # chroma_cens_var.at[id] = np.var(chroma_cens)
        mel_mean.at[id] = np.mean(melspectrogram)  # melspectrogram 梅尔频谱
        # mel_std.at[id] = np.std(melspectrogram)
        mel_var.at[id] = np.var(melspectrogram)
        mfcc_mean.at[id] = np.mean(mfcc)  # mfcc MFCC特征
        # mfcc_std.at[id] = np.std(mfcc)
        mfcc_var.at[id] = np.var(mfcc)
        mfcc_delta_mean.at[id] = np.mean(mfcc_delta)  # mfcc delta
        # mfcc_delta_std.at[id] = np.std(mfcc_delta)
        mfcc_delta_var.at[id] = np.var(mfcc_delta)
        rmse_mean.at[id] = np.mean(rmse)  # rmse
        # rmse_std.at[id] = np.std(rmse)
        rmse_var.at[id] = np.var(rmse)
        cent_mean.at[id] = np.mean(cent)  # cent
        # cent_std.at[id] = np.std(cent)
        cent_var.at[id] = np.var(cent)
        spec_bw_mean.at[id] = np.mean(spec_bw)  # spectral bandwidth
        # spec_bw_std.at[id] = np.std(spec_bw)
        spec_bw_var.at[id] = np.var(spec_bw)
        contrast_mean.at[id] = np.mean(contrast)  # contrast
        # contrast_std.at[id] = np.std(contrast)
        contrast_var.at[id] = np.var(contrast)
        rolloff_mean.at[id] = np.mean(rolloff)  # rolloff
        # rolloff_std.at[id] = np.std(rolloff)
        rolloff_var.at[id] = np.var(rolloff)
        poly_mean.at[id] = np.mean(poly_features)  # poly features
        # poly_std.at[id] = np.std(poly_features)
        poly_var.at[id] = np.var(poly_features)
        tonnetz_mean.at[id] = np.mean(tonnetz)  # tonnetz
        # tonnetz_std.at[id] = np.std(tonnetz)
        tonnetz_var.at[id] = np.var(tonnetz)
        zcr_mean.at[id] = np.mean(zcr)  # zero crossing rate
        # zcr_std.at[id] = np.std(zcr)
        zcr_var.at[id] = np.var(zcr)
        harm_mean.at[id] = np.mean(harmonic)  # harmonic
        # harm_std.at[id] = np.std(harmonic)
        harm_var.at[id] = np.var(harmonic)
        perc_mean.at[id] = np.mean(percussive)  # percussive
        # perc_std.at[id] = np.std(percussive)
        perc_var.at[id] = np.var(percussive)
        frame_mean.at[id] = np.mean(frames_to_time)  # frames
        # frame_std.at[id] = np.std(frames_to_time)
        frame_var.at[id] = np.var(frames_to_time)

        # print(frame_var)

        id += 1

    # 合并所有特征并转换成csv, json文件
    feature_set['label'] = labels
    feature_set['emotion_id'] = emotion_vector
    feature_set['song_name'] = songname_vector  # song name
    feature_set['tempo'] = tempo_vector  # tempo
    feature_set['total_beats'] = total_beats  # beats
    feature_set['average_beats'] = average_beats
    feature_set['chroma_stft_mean'] = chroma_stft_mean  # chroma stft
    # feature_set['chroma_stft_std'] = chroma_stft_std
    feature_set['chroma_stft_var'] = chroma_stft_var
    # feature_set['chroma_cq_mean'] = chroma_cq_mean  # chroma cq
    # feature_set['chroma_cq_std'] = chroma_cq_std
    # feature_set['chroma_cq_var'] = chroma_cq_var
    # feature_set['chroma_cens_mean'] = chroma_cens_mean  # chroma cens
    # feature_set['chroma_cens_std'] = chroma_cens_std
    # feature_set['chroma_cens_var'] = chroma_cens_var
    feature_set['melspectrogram_mean'] = mel_mean  # melspectrogram
    # feature_set['melspectrogram_std'] = mel_std
    feature_set['melspectrogram_var'] = mel_var
    feature_set['mfcc_mean'] = mfcc_mean  # mfcc
    # feature_set['mfcc_std'] = mfcc_std
    feature_set['mfcc_var'] = mfcc_var
    feature_set['mfcc_delta_mean'] = mfcc_delta_mean  # mfcc delta
    # feature_set['mfcc_delta_std'] = mfcc_delta_std
    feature_set['mfcc_delta_var'] = mfcc_delta_var
    feature_set['rmse_mean'] = rmse_mean  # rmse
    # feature_set['rmse_std'] = rmse_std
    feature_set['rmse_var'] = rmse_var
    feature_set['cent_mean'] = cent_mean  # cent
    # feature_set['cent_std'] = cent_std
    feature_set['cent_var'] = cent_var
    feature_set['spec_bw_mean'] = spec_bw_mean  # spectral bandwidth
    # feature_set['spec_bw_std'] = spec_bw_std
    feature_set['spec_bw_var'] = spec_bw_var
    feature_set['contrast_mean'] = contrast_mean  # contrast
    # feature_set['contrast_std'] = contrast_std
    feature_set['contrast_var'] = contrast_var
    feature_set['rolloff_mean'] = rolloff_mean  # rolloff
    # feature_set['rolloff_std'] = rolloff_std
    feature_set['rolloff_var'] = rolloff_var
    feature_set['poly_mean'] = poly_mean  # poly features
    # feature_set['poly_std'] = poly_std
    feature_set['poly_var'] = poly_var
    feature_set['tonnetz_mean'] = tonnetz_mean  # tonnetz
    # feature_set['tonnetz_std'] = tonnetz_std
    feature_set['tonnetz_var'] = tonnetz_var
    feature_set['zcr_mean'] = zcr_mean  # zero crossing rate
    # feature_set['zcr_std'] = zcr_std
    feature_set['zcr_var'] = zcr_var
    feature_set['harm_mean'] = harm_mean  # harmonic
    # feature_set['harm_std'] = harm_std
    feature_set['harm_var'] = harm_var
    feature_set['perc_mean'] = perc_mean  # percussive
    # feature_set['perc_std'] = perc_std
    feature_set['perc_var'] = perc_var
    feature_set['frame_mean'] = frame_mean  # frames
    # feature_set['frame_std'] = frame_std
    feature_set['frame_var'] = frame_var

    # feature_set.to_csv('EmotionFeatures.csv')
    # feature_set.to_json('EmotionFeatues.json')
    return feature_set


# 四种主要的情绪：1-sad, 2-happy, 3-relax, 4-angry
if __name__ == '__main__':
    fs = pd.DataFrame()
    startid = 1
    sad_fs = extract_features('sad\\', 'sad', 1, startid)
    fs = fs.append(sad_fs)
    startid += len(listdir('sad'))
    happy_fs = extract_features('happy\\', 'happy', 2, startid)
    fs = fs.append(happy_fs)
    startid += len(listdir('happy'))
    relax_fs = extract_features('relax\\', 'relax', 3, startid)
    fs = fs.append(relax_fs)
    startid += len(listdir('angry'))
    excited_fs = extract_features('angry\\', 'angry', 4, startid)
    fs = fs.append(excited_fs)

    # 保存成文件
    fs.to_csv('EmotionFeatures.csv')
