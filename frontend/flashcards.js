
var state = "";

function renderWord(data) {
  $("#word").html("<h2>" + data.word + "</h2>");
  $("#definition").html("<h2>" + data.definition + "</h2>");
  $("#definition").hide();
}

function renderAnswer(data) {
  $("#word").html("<h2>" + data.word + "</h2>");
}

function renderInterface(data) {
}

function resetAllCards() {
}

function reviewCardCorrect() {
}

function reviewCardWrong() {
}

function getNextCard() {
  $.ajax({
    url : 'http://localhost:8000/api/next/',
    type : 'GET',
    dataType:'json',
    'success' : function(data) {
      console.log(data);
      renderCard(data);
    },
    'error' : function(data) {
      console.log(data);
    }
  });
}

$(document).ready(function() {
  state = "guess";
  getNextCard();
});

