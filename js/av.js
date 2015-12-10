/**
 * Easy av.
 */

var g_playerName; // player name
var g_gamekey; // game key

var setName_ = function (name) {
    g_playerName = name;
    $('#name').text(name)
    $('#addplayer').addClass('hid');
    $('#info').removeClass('hid');
    refresh();
};

var handleJoinGame = function() {
    var game = $('#gamename').val();
    if (game) {
        g_gamekey = game;
        console.log('joining game:', game);
        $('#gamebutton').addClass('hid');
    }
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
        $.post('/ppl', {name:name}, addPlayerSuccess.bind(this, name));
    }
};

var claim = function(name) {
    console.log('claim:', name);
    setName_(name);
}

var refresh = function() {
	$.get('ppl', {player: g_playerName}, function(data) {
		console.log('ppl:', data);
		$('#role').text(data['role'] ? data['role'] : '?');
		$('#people').empty();
		$.each(data['people'], function(i, name) {
			var append = '';
			if (!g_playerName) {
			    append = ' <a href="javascript:claim(\'' + name + '\')">claim player</a>';
			}
			$('#people').append('<li>' + name + append);
		    });
        
		$('#sees').empty();
		if (data['sees']) {
		    $.each(data['sees'], function(i, name) {
			    $('#sees').append('<li>' + name);
			});
		}
	    });
      
	$.get('role', function(data) {
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
	$('#gamebutton').click(handleJoinGame);
	$('#playerbutton').click(handleAddPlayer);
	$('#toggle').click(toggle);
     
	$('#refreshbutton').click(refresh);
	setInterval(refresh, 1000);
	// refresh();
    });
