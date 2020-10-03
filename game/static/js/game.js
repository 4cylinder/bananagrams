function copyToClipboard(text) {
  var $temp = $("<input>");
  $("body").append($temp);
  $temp.val(text).select();
  document.execCommand("copy");
  $temp.remove();
}

function pollForEvents(eventUrl, playerStateUrl) {
  return setInterval(function(){
    $.get(eventUrl, function( data ) {
      var event = data.event;
      var tilesLeft = data.tilesLeft;
      // delete microseconds
      var eventTime = event.time.split(".")[0];
      var eventInfo = event.info;
      var newEvent = eventTime + ": " + eventInfo;
      var mostRecent = $('.game-event').last().text();
      if (mostRecent != newEvent) {
        $('#event-container').append("<p class='game-event'>" + newEvent + "</p>");
        console.log("new");
        switch (event.event_type) {
          case 'FULL':
            $('#startBtn').prop('disabled', false);
            break;
          case 'START':
            $('#startBtn').prop('disabled', true);
            $('#startBtn').hide();
          case 'PEEL':
          case 'DUMP':
            updatePlayerState(playerStateUrl);
            break;
          case 'WIN':
            console.log("end game for all");
            break;
        }
      }
    });
  }, 1000);
}

function updatePlayerState(playerStateUrl) {
  $.post(playerStateUrl, function( data ) {
    var rack = data.rack;
    console.log(data);
  });
}
