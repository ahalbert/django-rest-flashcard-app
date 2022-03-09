
var state = "";
var currentCardId;

function renderWord(data) {
  if ("message" in data) {
    $("#interface").hide();
    $("#card-definition").hide();
    if (data.message == "cards temporarily done.") {
      $("#card-word").html("<h2>You are temporarily done; please come back later to review more words.</h2>");
    }
    else if (data.message == "all cards done.") {
      $("#card-word").html("<h2>you have no more words to review; you are permanently done!</h2>");
    }
    else {
      renderError(data);
    }
  }
  else {
    currentCardId = data.id;
    $("#card-word").html("<h2>" + data.word + "</h2>");
    $("#card-definition").html("<h3> Definition: " + data.definition + "</h3>");
    $("#interface").html("<button onclick=renderAnswer()>Show Answer</button>");
    $("#card-definition").hide();
  }
}

function renderAnswer() {
  $("#card-definition").show();
  $("#interface").html("<button onclick=reviewCard(true)>I got it right</button><button onclick=reviewCard(false)>I got it wrong</button>");
}

function renderError(data) {
  $("#card-word").html("There was an error. Try refreshing your browser.");
  $("#card-definition").hide();
  $("#interface").hide();
}

function resetAllCards() {
}

function reviewCard(isCorrect) {
  $.ajax({
    url : 'http://ahalbert.com:8000/api/review/',
    type : 'POST',
    data : {"isCorrect" : isCorrect, "id" : currentCardId},
    dataType:'json',
    'success' : function(data) { },
    'error' : function(data) {
      console.log(data);
    }
  });
  getNextCard();
}



function getNextCard() {
  $.ajax({
    url : 'http://ahalbert.com:8000/api/next/',
    type : 'GET',
    dataType:'json',
    'success' : function(data) {
      renderWord(data);
    },
    'error' : function(data) {
      console.log(data);
    }
  });
}

$(document).ready(function() {
  getNextCard();
});

