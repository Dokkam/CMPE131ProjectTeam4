var start = document.getElementById('start');
var stop  = document.getElementById('stop');
var reset = document.getElementById('reset');
var breakMin = document.getElementById('break_minutes');
var breakSec = document.getElementById('break_seconds');

//store a reference to a timer variable
var startTimer;

start.addEventListener('click', function(){
    if(startTimer === undefined){
        startTimer = setInterval(timer, 1000)
    } else {
        alert("Timer is already running, Press Ok to continue");
    }
})

reset.addEventListener('click', function(){
    breakMin.innerText = 5;
    breakSec.innerText = "00";

    document.getElementById('counter').innerText = 0;
    stopInterval()
    startTimer = undefined;
})

stop.addEventListener('click', function(){
    stopInterval()
    startTimer = undefined;
})


//Start Timer Function
function timer(){
    if(breakSec.innerText != 0){
        breakSec.innerText--;
    } else if(breakMin.innerText != 0 && breakSec.innerText == 0){
        breakSec.innerText = 59;
        breakMin.innerText--;
    }
}

//Stop Timer Function
function stopInterval(){
    clearInterval(startTimer);
}