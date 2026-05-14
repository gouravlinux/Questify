// security.js

const securityQuizForm =
    document.getElementById("quizForm");



function autoSubmitQuiz(message) {

    alert(message);

    if (securityQuizForm) {

        securityQuizForm.submit();

    }

}



// TAB SWITCH DETECTION

document.addEventListener(
    "visibilitychange",
    () => {

        if (document.hidden) {

            autoSubmitQuiz(
                "⚠ Tab switching detected. Quiz will be submitted."
            );

        }

    }
);



// RIGHT CLICK DISABLE

document.addEventListener(
    "contextmenu",
    (e) => {

        e.preventDefault();

    }
);



// COPY DISABLE

document.addEventListener(
    "copy",
    (e) => {

        e.preventDefault();

    }
);



// CUT DISABLE

document.addEventListener(
    "cut",
    (e) => {

        e.preventDefault();

    }
);



// PASTE DISABLE

document.addEventListener(
    "paste",
    (e) => {

        e.preventDefault();

    }
);



// DEVTOOLS SHORTCUTS

document.addEventListener(
    "keydown",
    (e) => {

        if (
            e.key === "F12" ||

            (
                e.ctrlKey &&
                e.shiftKey &&
                e.key === "I"
            ) ||

            (
                e.ctrlKey &&
                e.shiftKey &&
                e.key === "J"
            ) ||

            (
                e.ctrlKey &&
                e.key === "U"
            )
        ) {

            e.preventDefault();

        }

    }
);