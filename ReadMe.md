#### 使用方法

- 将`mer2.py`和`EmotionFeatures2.csv`放置在同级目录中
- 导入`mer2.py`导入类`MusicEmotionRecognizer`

```python
from mer2 import MusicEmotionRecognizer
```

- 评分前，输入评分歌曲文件路径（如'song/test.mp3'），得出一个类别

```python
er = MusicEmotionRecognizer()
clas = er.predictEmotion('song/test.mp3')
```

- 录音结束后，输入录音文件路径（如'record/realtime.mp3'），得出一个类别

```python
clas2 = er.predictEmotion('song/test.mp3')
```

- 如果两个类别相同，则加上相应的分数（如情绪符合，则附加五分 ）

```python
if clas == clas2:
    score += 5
```

#### 依赖库

- numpy
- pandas
- librosa
- audioread
- sklearn