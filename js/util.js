var Util = {}

// Refreshes the list of games in the system.

/**
 * @param {string} containerSelector Selector for container element.
 */
Util.refreshGames = function(containerSelector) {
  $.get('/game', {}, function(data) {
    var containerEl = $(containerSelector);
    containerEl.empty();
    if (data['games']) {
      $.each(data['games'], function(i, game) {
        containerEl.append('<li>' + game['key'] +
          ' <span class="note">(' + game['time'] + ')</span>');
      });
    }
  });
};


/**
 * @param {string} targetSelector
 */
Util.toggle = function(targetSelector) {
  $(targetSelector).toggleClass('hid');
};