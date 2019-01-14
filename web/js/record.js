var recorder = document.getElementById("recorder");
var accuracyScoreSpan = document.getElementById("accuracyScoreSpan");
var rhythmScoreSpan = document.getElementById("rhythmScoreSpan");
var originalEmotionSpan = document.getElementById("originalEmotionSpan");
var meEmotionSpan = document.getElementById("meEmotionSpan");

var flag = false;

function setScore2(score) {
	accuracyScoreSpan.innerHTML = String(score[0]).substr(0, 5);
	rhythmScoreSpan.innerHTML = String(score[1]).substr(0, 5); 
}

function setScore(){
	eel.getScore()(setScore2);
}


function startRecord(){
	alert("录音开始");
	console.log("startRecord");
	eel.initRecorder();
	Timer = window.setInterval(setScore, 10000);
	recorder.setAttribute("src", "banzou_2.mp3");
	recorder.currentTime = 0;
	recorder.play();
	
	flag = false;
};

function stopRecord(){
	alert("录音结束");
	console.log("stopRecord");
	eel.stopRecorder();
	Timer = window.clearInterval(Timer);
	recorder.pause();
	recorder.currentTime = 0;

	flag = true;
}

function playRecord(){
	console.log("moodAnalyze");
	if(flag == false){
		alert("请先停止录音");
		return;
	}
	console.log("playRecord");
	recorder.setAttribute("src", "record.wav");
	recorder.currentTime = 0;
	recorder.play();
}

function stopPlayRecord(){
	console.log("stopPlayRecord");
	recorder.pause();
	recorder.currentTime = 0;
}

function setOriginalEmotion(emotionStr){
	console.log("original: " + emotionStr);
	originalEmotionSpan.innerHTML = emotionStr;
}

function setEmotion(emotionStr){
	console.log("me: " + emotionStr);
	meEmotionSpan.innerHTML = emotionStr;
}

function moodAnalyze(){
	console.log("moodAnalyze");
	if(flag == false){
		alert("请先停止录音");
		return;
	}
	alert("正在分析请稍等...");
	eel.getOriginalEmotion()(setOriginalEmotion);
	eel.getEmotion()(setEmotion);
}
