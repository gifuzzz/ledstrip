const post = (url, data, clicked) => {
    $.ajax({
        type: "POST",
        url: url,
        data: data,
        success: function (result) {
            console.log('res: ' + result);
            if (result === 'ok') {
                console.log(clicked[0])
                if (clicked[0].className.includes('btn-outline-')) {
                    clicked[0].className = clicked[0].className.replace('btn-outline-', 'btn-')
                } else {
                    clicked[0].className = clicked[0].className.replace('btn-', 'btn-outline-')
                }
            }
        },
        error: function (result) {
            console.log('error: ' + result.error);
        }
    });
}

$('.dev').click(function () {
    $('.dev').each(dev => {
        if (!$('.dev')[dev].className.includes('btn-outline-')) {
            $('.dev')[dev].className = $('.dev')[dev].className.replace('btn-', 'btn-outline-')
        }
    })
    var mac = $(this).text();
    console.log(mac + ' clicked!');
    post('/setmac', { mac: mac }, $(this))
});