const AnswerButton = document.getElementById("AnswerButton");
const RatingSelection = document.getElementById("RatingSelection");

RatingSelection.style.display = "none";
AnswerButton.addEventListener('click', function(e) {
    console.log("button pressed");
    RatingSelection.style.display = "block";

});
