
function sendServoRequest(direction) {
    console.log('request');
    $.ajax({
        type: 'POST',
        url: '/servo',
        data: {
            'direction': 'left',
            'degrees': $('#degrees').value
        },
        success: (data) => {
            console.log('success');
        },
    });
}

