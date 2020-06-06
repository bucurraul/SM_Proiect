
function sendServoRequest(direction) {
    $.ajax({
        type: 'POST',
        url: '/servo',
        data: {
            'direction': 'left',
            'degrees': $('#degrees').val()
        },
    });
}


function updateDegreesBox(value) {
    $('#degrees_box').val(value);
}

