var assign = function() {
  $.post('/role', {assign:1}, function(data) {
    console.log('assigned roles:', data);
  });
  location.reload();
};

var addGame = function() {
  console.log('button clicked!');
  var key = $('#gamekey').val();
  console.log('adding game: ', key);
  $.post('/game', {create:1, gamekey: key}, function(data) {
    console.log('create game:', data);
    Util.refreshGames('#games');
  });
  // location.reload();
};


$(document).ready(function() {
  $('#gamebutton').click(addGame);
  $('#assign').click(assign);
  $('#toggle').click(Util.toggle.bind(this, '#people'));

  Util.refreshGames('#games');
});

console.log('loaded admin script');