const get = (url) => {
    $.ajax({
        type: "GET",
        url: url,
        success: function (result) {

        },
        error: function (result) {
            // alert('error: ' + result.error);
        }
    });
}

const post = (url, data) => {
    $.ajax({
        type: "POST",
        url: url,
        data: data,
        success: function (result) {
            console.log('res: ' + result)
        },
        error: function (result) {
            console.log('error: ' + result.error);
        }
    });
}

var colorPicker = $('#color-picker')

colorPicker.spectrum({
    type: "component",
    showInput: true,
    showAlpha: false,
    preferredFormat: "hex",
    move: () => {
        changeColor();
    }
});

var d = new Date()
var last = d.getTime()
var changeColor = () => {
    updateAll(colorPicker.val())
    d = new Date()
    var now = d.getTime()
    if (now - last > 50) {
        last = now;
        get("/rgb?hex=" + colorPicker.val().slice(1))
    }
}

function updateAll(color) {
    document.querySelectorAll("p").forEach(function (p) {
        p.style.color = color;
    });
    $('#slider .ui-slider-range, #sliderspeed .ui-slider-range').css('background', colorPicker.val())
    $('#slider .ui-slider-handle, #sliderspeed .ui-slider-handle').css('border-color', colorPicker.val())
}

var slider = $("#slider");
slider.slider({
    animate: "fast",
    max: 100,
    value: 75,
    range: "min",
    slide: () => changeBrightness(),
    change: () => changeBrightness(),
});

var changeBrightness = () => {
    d = new Date()
    var now = d.getTime()
    if (now - last > 50) {
        last = now
        get("/lum?lvl=" + slider.slider('value'))
    }
}
var sliderspeed = $("#sliderspeed");
sliderspeed.slider({
    animate: "fast",
    max: 100,
    value: 75,
    range: "min",
    slide: () => changeSpeed(),
    change: () => changeSpeed(),
});

var changeSpeed = () => {
    d = new Date()
    var now = d.getTime()
    if (now - last > 50) {
        last = now
        get("/speed?val=" + sliderspeed.slider('value'))
    }
}

$('#checkbox').change(() => {
    if ($('#checkbox').is(":checked")) {
        get('/on')
    } else {
        get('/off')
    }
})

$('.mode').click(function() {
    get('/mode?mode=' + this.id)
})

$('#changemac').click(() => {
    post('/setmac', { mac: $('#mac').val() })
})