setInterval(() => {
    $.ajax({
        type: 'GET',
        url: '/get-angles',
        success: (response) => { 
            let results = JSON.parse(response);

            degrees0 = results[0];
            degrees1 = results[1];

            $('#degrees_box0').val(degrees0);
            $('#degrees_box1').val(degrees1);

            $('#degrees0').val(degrees0);
            $('#degrees1').val(degrees1);
        },
    });
}, 1000);


function updateDegreesBox(servo, value) {
    $('#degrees_box' + servo).val(value);
    console.log("Mesaj");
    $.ajax({
        type: 'POST',
        url: '/servo/' + servo,
        data: {
            'degrees': $('#degrees' + servo).val()
        },
        success: () => { console.log("Lambda0 OK")},
    });
}


function toggleLight(number) {
    $.ajax({
        type: 'POST',
        url: '/light/' + number,
        success: () => console.log("Toggle light OK")
    });
}

