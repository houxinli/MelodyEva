var recorder;
var audio = document.querySelector('audio');
var accuracyScoreSpan = document.getElementById("accuracyScoreSpan");
var rhythmScoreSpan = document.getElementById("rhythmScoreSpan");

function setScore2(score) {
	accuracyScoreSpan.innerHTML = String(score[0]).substr(0, 5);
	rhythmScoreSpan.innerHTML = String(score[1]).substr(0, 5); 
}

function setScore(){
	eel.getScore()(setScore2);
}


function startRecord(){
	console.log("startRecord");
	eel.initRecorder();
	HZRecorder.get(function(rec){
		recorder = rec;
		recorder.start();
	});
	window.setInterval(setScore, 10000);
};

function stopRecord(){
	console.log("stopRecord");
	eel.stopRecorder();
	recorder.stop();
}

function playRecord(){
	console.log("playRecord");
	recorder.play(audio);
}

