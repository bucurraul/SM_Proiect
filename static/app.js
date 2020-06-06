
function sendServoRequest(direction) {
    console.log('request');
    $.ajax({
        type: 'POST',
        url: '/servo',
        data: {
            'direction': direction,
            'degrees': $('#degrees').value
        },
        success: (data) => {
            console.log('success');
        },
    });
}

