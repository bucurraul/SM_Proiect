
function updateDegreesBox(value) {
    $('#degrees_box').val(value);

    $.ajax({
        type: 'POST',
        url: '/servo',
        data: {
            'degrees': $('#degrees').val()
        },
    });
}

