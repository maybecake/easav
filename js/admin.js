var assign = function() {
  $.post('/role', {assign:1}, function(data) {
    console.log('assigned roles:', data);
  });
  location.reload();
};

var addGame = function() {
  var key = $('#gamekey').val();
  $.post('/game', {create:1, gamekey: key}, function(data) {
    console.log('create game:', data);
  });
  location.reload();
}

var toggle = function() {
  $('#people').toggleClass('hid');
};

$(document).ready(function() {
  $('#gamebutton').click(addGame);
  $('#assign').click(assign);
  $('#toggle').click(toggle);
});
