/* Open Chat by @faustinoaq
 * This code use Jquery library
 */

var textarea = $('#content');
var messages = $('#chat');
var Limit = 1024;

// Send form message without reload the page
$(document).on('submit', '#form' , function() {
    var form = $('#form');
    var data = form.serialize().slice(0, Limit + 8);
    console.log(textarea.val());
    $.post('/', data, function() {
        $('#content').val('');
        $('#characters').text(0);
    });
    return false;
});

$(document).on('keydown mouseout', '#content' , function() {
    var Size = textarea.val().length;
    console.log(Size);
    $('#characters').text(Size);
    if (Size >= Limit) {
      var value = textarea.val();
      textarea.val(value.slice(0, Limit));
      console.log("textarea (MAX LIMIT is 10000 characters)");
    }
});

function toGo(url) {
  window.location = window.location + url;
}

var isFirst = true;
var messageReport = 0;
var messageCounter = 0;

function Update() {
  $.get('/data/report', function(json) {
    eval(json);
    console.log(report);
    $('#clients').text(report['clients']);
    if (isFirst) {
      messageCounter = report['messages'];
      isFirst = false;
      console.log("Loading all messages...");
      $.get('/data/recent-messages', function(data) {
        messages.html(data);
      });
    } else {
      messageReport = report['messages'];
      if (messageReport == messageCounter) {
        console.log("Nothing to update");
      } else if (messageReport > messageCounter || messageReport < messageCounter) {
        $.get('/data/last-message', function(data) {
          console.log("Loading last message: ", data);
          messages.prepend(data);
          messageCounter = messageReport;
        });
      }
    }
  });
}

setInterval(Update, 500);
