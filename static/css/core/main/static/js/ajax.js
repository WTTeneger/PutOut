function auth() {
    url = '/api/account/auth/'
    data = {
        'username':document.getElementById('user-login').value,
        'password':document.getElementById('user-pass').value
    }
    localize = '/' + location.pathname.split('/')[1]
    u = location.origin + localize + url
    $.post(u, data, function (data) {
    }).done(function (data) {
        console.log(data);
        window.location.href = location.origin + localize + '/app/dashboard/'
    }).fail(function (data) {
        data = data['responseJSON']
        console.log(data);
    })
    //     .always(function(data) {
    //     console.log(data);
    // });
}

t = 0
var status_timer_sms = false

function register(el) {
    localize = '/' + location.pathname.split('/')[1]
    console.log(localize)
    let url = '/my_send_mail/?email=' + document.getElementById('user-login').value
    let u = location.origin + localize + url
    console.log(u)
    $.post(u, function () {
    })
    T = 25

    function timers(t) {
        if (t == T) {
            status_timer_sms = true
            el.children[0].style = 'filter: invert(.1);'
            el.disabled = true
            el.children[1].style.display = 'Block';
        }
        if (t != 0) {
            el.children[1].innerHTML = t
            window.setTimeout(timers, 1000, t - 1);
        } else {
            el.children[0].style = ''
            el.disabled = false
            el.children[1].style.display = 'None';
            status_timer_sms = false
        }
    }

    if (!status_timer_sms) {
        window.setTimeout(timers, 50, T);
    }

}
