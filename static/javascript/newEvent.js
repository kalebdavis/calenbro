var submitButton = document.getElementsByClassName("createNewEventButton")[0];
submitButton.addEventListener("click", function(e) {
  e.preventDefault();

  var data = {
    name: document.getElementsByClassName("eventName")[0].value,
    startDate: document.getElementsByClassName("startDate")[0].value,
    endDate: document.getElementsByClassName("endDate")[0].value
  }

  console.log(data)

  var request = new XMLHttpRequest();
  request.open('POST', '/event/create', true);
  request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
  request.send(data);
});
