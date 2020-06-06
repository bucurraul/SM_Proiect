
function updateDegreesBox(value) {
    $('#degrees_box').val(value);
    console.log("Mesaj")
    $.ajax({
        type: 'POST',
        url: '/servo',
        data: {
            'degrees': $('#degrees').val()
        },
	success: () => { console.log("Lambda OK")},
    });
}

