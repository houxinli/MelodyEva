var recorder;
var audio = document.querySelector('audio');
var accuracyScoreSpan = document.getElementById("accuracyScoreSpan");
var rhythmScoreSpan = document.getElementById("rhythmScoreSpan");

function startRecord(){
	console.log("startRecord");
	//eel.initRecorder();
	HZRecorder.get(function(rec){
		recorder = rec;
		recorder.start();
	});
};

function stopRecord(){
	console.log("stopRecord");
	//eel.stopRecorder();
	recorder.stop();
}

function playRecord(){
	console.log("playRecord");
	recorder.play(audio);
}

function setAccuracyScore(score){
	accuracyScoreSpan.innerHTML = score;
}

function setRhythmScore(score){
	rhythmScoreSpan.innerHTML = score;
}

