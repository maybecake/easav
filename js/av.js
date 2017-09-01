/**
 * Easy av.
 */

var g_playerName;  // player name
var g_gamekey;     // game key

var setName_ = function (name) {
    g_playerName = name;
    $('#name').text(name)
    $('#addplayer').addClass('hid');
    $('#info').removeClass('hid');
    refresh();
};


var addPlayerSuccess = function(name, data) {
    console.log('added player successfully:', data);
    if (data['error']) {
        console.error('add player error: ', data['error'])
	    } else {
        setName_(name);
        refresh();
    }
};

var handleAddPlayer = function() {
    var name = $('#playername').val();
    if (name) {
        console.log('Try to add:', name);
        $.post('/ppl', {gamekey: g_gamekey, name: name}, addPlayerSuccess.bind(this, name));
    }
};


var claim = function(name) {
    console.log('claim:', name);
    setName_(name);
};


/**
 * Gets a list of games from the server and presents them as a dropdown.
 * Once a game has been selected, it can no longer be changed unless the
 * user reloads.
 */
var getGames_ = function() {
  $.get('game', {}, function(data) {
    var options = $('#gamesDropdown');
    options.empty();
    options.append($('<option />').val('').text('Select a game'));
    if (data['games']) {
      $.each(data['games'], function() {
        options.append($('<option />').val(this['key']).text(this['key']));
      });

      $('#gamesDropdown').on('change', function() {
        if (this.value) {
          g_gamekey = this.value;
          console.log('game key set:', g_gamekey);
          $(this).off('change').prop('disabled', true);
          refresh();
        }
      });
    }
  });
};


/**
 * Refreshes the data on the page.
 * 
 */
var refresh = function() {
	$.get('ppl', {gamekey: g_gamekey, player: g_playerName}, function(data) {
		console.log('ppl:', data);
		$('#role').text(data['role'] ? data['role'] : '?');
		$('#people').empty();
		$.each(data['people'], function(i, name) {
			var listItem = $('<li>');
			listItem.text(name + ' ');
			if (!g_playerName) {
			    var claimLink = $('<a/>');
			    claimLink.attr('href', 'javascript:void;');
			    claimLink.text('claim player');
			    claimLink.click(function (e) {
			        e.preventDefault();
			        claim(name);
			    });
			    listItem.append(claimLink);
			}
			$('#people').append(listItem);
		    });
        
		$('#sees').empty();
		if (data['sees']) {
		    $.each(data['sees'], function(i, name) {
			    $('#sees').append('<li>' + name);
			});
		}
	    });
      
	$.get('role', {gamekey: g_gamekey}, function(data) {
		console.log('roles:', data);
		$('#roles').empty();
		$.each(data['roles'], function(i, role) {
			$('#roles').append('<li>' + role['info']['name'] +
					   ': <span class="roleinfo">' + role['info']['desc'] + '</span>');
		    });
	    });
    };
    
var toggle = function() {
    $('#secret').toggleClass('hid');
};


$(document).ready(function() {
	$('#playerbutton').on('click', handleAddPlayer);
	$('#toggle').click(toggle);
     
	$('#refreshbutton').click(refresh);

  getGames_();
	// setInterval(refresh, 1000);
	// refresh();
});
