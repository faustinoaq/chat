$(document).on('submit','#form',function(e) {
    var form = $('#form');
    var data = form.serialize();
    $.post('/', data, function(res) {
        $('#input').val('');
    });
    return false;
});

function update() {
    $.get('/update', function(data) {
        $('#chat').html(data);
    });
};

setInterval('update()', 1000);
