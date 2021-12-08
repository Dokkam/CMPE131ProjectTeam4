var start = document.getElementById('start');
var stop  = document.getElementById('stop');
var reset = document.getElementById('reset');

var workMin = document.getElementById('work_minutes');
var workSec = document.getElementById('work_seconds');

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
    workMin.innerText = 25;
    workSec.innerText = "00";

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
    if(workSec.innerText != 0){
        workSec.innerText--;
    } else if(workMin.innerText != 0 && workSec.innerText == 0){
        workSec.innerText = 59;
        workMin.innerText--;
    }
}

//Stop Timer Function
function stopInterval(){
    clearInterval(startTimer);
}