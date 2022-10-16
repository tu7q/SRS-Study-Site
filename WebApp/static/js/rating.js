const AnswerButton = document.getElementById("AnswerButton");
const RatingSelection = document.getElementById("RatingSelection");

console.log("working");
console.log("AnswerButton", AnswerButton);
console.log("RatingSelection", RatingSelection);

RatingSelection.style.display = "none";
AnswerButton.addEventListener('click', function(e) {
    console.log("button pressed");
    RatingSelection.style.display = "block";

});
