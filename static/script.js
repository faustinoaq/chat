/* Javascript Code by @faustinoaq
 * This code use Jquery 2.1.3
 */


// Send form message without reload the page
$(document).on('submit','#form',function(e) {
    var form = $('#form');
    var data = form.serialize();
    $.post('/', data, function(res) {
        $('#input').val('');
    });
    return false;
});


// Delete all messages * Require login
function Delete() {
  $.get('/delete', function(res) {
      console.log("Delete messages");
      window.location = window.location;
  });
  return false;
}


/* Functions for update the messages
 * 1. Check the amount of entries in database
 * 2. Compare initial amount with the last amounts
 * 3. Update if amounts are differents
 */

var COUNT = "0";  // Default amount of entries
var COUNTER = "0";  // Function to check amount
var Current = "0"; // Save counter changes

function update() {
  if (Current === COUNTER) {
    console.log("Nothing to update");
  } else {
    console.log("Updating...");
    $.get('/update', function(data) {
      console.log("Update: ", data);
      $('#chat').prepend(data);
      Current = COUNTER;
      console.log("Current amount: ", Current);
    });
  }
}

function counter() {
  if (COUNT == "0") {
    $.get('/count', function(data) {
      Current = data;
      console.log("First count:", Current);
    });
    $.get('/update', function(data) {
      console.log("Updating...");
      console.log("Update: ", data);
      $('#chat').append(data);
    });
    COUNT = "1";
  } else {
    $.get('/count', function(data) {
      COUNTER = data;
      console.log("Counter: ", COUNTER);
      update();
    });
  }
}

setInterval(counter, 500);
