新闻联播文字版：http://www.xwlbo.com/

新闻联播的youtube首页：https://www.youtube.com/channel/UCcLK3j-XWdGBnt5bR9NJHaQ

下载youtube视频的网址：https://zh.savefrom.net/7/ 

#---------------------------------------- 新闻联播数据集处理步骤 ------------------------------------------------------------

参考资料： https://liuziyi219.github.io/2019/06/08/Chinese-Pipeline-Week1/

step1： convert mp4 to wav (RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 32000 Hz)
	
	ffmpeg -i example.mp4 -hide_banner -loglevel 0 -ac 1 -ar 32000 example.wav     # 通道数=1, 采样率=32000
	
step2:   Split the audio
	
	python3 audiosplit.py <padding duration> <path to wav file/directory> <path to directory>
	python3 audiosplit.py 300 example.wav output/   # padding duration: 原作者多次测试，发现300是比较合适的值, 可取200ms, 250ms, 280ms, 300ms
   Usually, the result won’t be satisfied after the first split. Some of cuts will be quite long. To deal with the audios that are longer than 30 seconds(or you can change into other standards), you can decrease the padding duration and re-split them. You don’t need to select them by yourself. Just assign the directory including all the files, and all audio that are longer than 30s would be selected and re-splitted.
当然，也可以使用 audiosplit_once.py 来直接分割音频。它里面内置的while循环，会尝试多个padding duration参数来对时长大于30秒的音频进行分割。


