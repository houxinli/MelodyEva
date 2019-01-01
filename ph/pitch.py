#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import numpy as np, scipy, matplotlib.pyplot as plt, IPython.display as ipd
import librosa, librosa.display
import math

# acf and deal with voice
def deal1(path):
    x, sr = librosa.load(path)  # read the voice

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
    # tanslate 10ms motes into 100ms notes

    nt0 = np.empty([int(max0 / 10 - 1), ], dtype=float)
    for i in range(0, int(max0 / 10 - 1)):
        ns = 0
        count1 = 0
        for j in range(0, 10):
            if n0[i * 10 + j] > 0:
                ns += n0[i * 10 + j]
                count1 += 1
        if count1 <= 9:
            nt0[i] = 0
        else:
            nt0[i] = float(ns) / count1

    # minus the zero in the front fo and the the last of the array
    for i in range(0, len(nt0)):
        if nt0[i] != 0:
            nt0 = nt0[i:]
            break
    for i in range(0, len(nt0)):
        if nt0[len(nt0) - 1 - i] != 0:
            nt0 = nt0[:(len(nt0) - i)]
            break
    return (nt0)


# test pitch
def pitch1(path1, path2):
    nt0 = deal1(path1)
    nt1 = deal1(path2)
    # choose the shortest voice

    scale = len(nt1) / len(nt0)
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
    print ("pitch_mark1:")
    print (pitch_mark1)
    return pitch_mark1

def Z_ScoreNormalization(x,mu,sigma):
    for i in range(0,12):
        x[i] = (x[i] - mu) / sigma
    return x

def deal2(path):
    x, sr = librosa.load(path)  # read the voice

    chroma = librosa.feature.chroma_stft(y=x, sr=sr)
    chroma = np.transpose(chroma)
    for i in range(0,len(chroma)):
        chroma[i] = Z_ScoreNormalization(chroma[i], np.average(chroma[0]), np.std(chroma[0]))
    return chroma

# test melody
def pitch2(path1, path2):
    chroma0 = deal2(path1)
    chroma1 = deal2(path2)
    chroma0 = np.transpose(chroma0)
    chroma1 = np.transpose(chroma1)

    D, wp = librosa.sequence.dtw(chroma0,chroma1,subseq=True)
    pitch_mark2 = 1 - math.atan(D[len(chroma0),len(chroma1)]/100) * 2 / math.pi
    print ("pitch_mark2:")
    print (pitch_mark2)
    return pitch_mark2
pitch_mark = 0.5*pitch1("../music_score/source_2.mp3","../music_score/test.wav") + 0.5*pitch2("../music_score/source_2.mp3","../music_score/test.wav")
print ("pitch_mark:")
print (pitch_mark)