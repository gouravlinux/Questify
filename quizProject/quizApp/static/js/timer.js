// timer.js

console.log("Timer JS Loaded");

const timerElement =
    document.getElementById("timer");

const timerQuizForm =
    document.getElementById("quizForm");



if (timerElement) {

    const quizTime =
        parseInt(
            timerElement.dataset.time
        ) || 1;

    let timeLeft =
        quizTime * 60;



    function updateTimer() {

        const minutes =
            Math.floor(timeLeft / 60);

        const seconds =
            timeLeft % 60;



        timerElement.innerText =
            `${minutes}:${
                seconds < 10
                ? "0" + seconds
                : seconds
            }`;



        if (timeLeft <= 0) {

            clearInterval(countdown);

            alert("⏰ Time is up!");

            if (timerQuizForm) {

                timerQuizForm.submit();

            }

            return;

        }



        timeLeft--;

    }



    const countdown =
        setInterval(updateTimer, 1000);



    updateTimer();

}