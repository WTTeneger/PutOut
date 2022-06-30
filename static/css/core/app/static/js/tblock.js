let bs;
let open_micro_modal;

var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
console.log($crf_token)
var sqr;

function sender(_target = '', _url, _type = 'GET', _data = {}, _header = {}) {
    console.log(_target)
    sqr = _target
    var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
    _header['X-CSRFToken'] = $crf_token
    $.ajax({
        type: _type,
        // make sure you respect the same origin policy with this url:
        // http://en.wikipedia.org/wiki/Same_origin_policy
        url: _url,
        data: _data,
        headers: _header,
        success: function (msg) {
            console.log(msg)
            if ('switch' in msg && msg['switch']){
                $(_target.parentElement.parentElement.parentElement).toggleClass('d-table__row--disabled');
            }
            if ('reload' in msg && msg['reload']){
                // window.location.reload();
            }
        }
    });
}

document.addEventListener('click', function (e) {
    console.log(e.target);
    console.log(e.target.getAttribute('Prodamus'));
    bs = e.target
    //  Открытие всплывающего окна
    if (e.target.getAttribute('data-micromodal-trigger')) {
        let elem = document.getElementById(e.target.getAttribute('data-micromodal-trigger'))
        console.log(elem)
        open_micro_modal = elem
        if (e.target.getAttribute('data-micromodal-trigger') == 'modal-confirm-delete') {
            let id = e.target.getAttribute('id-key')
            let url = location.pathname + 'remove/'+id
            document.getElementById('key-id').setAttribute('to-url', url)
            document.getElementById('key-name').innerText ='Удаление: ' + e.target.getAttribute('name-key')
        }
        elem.classList.add('is-open')
    }

    // Закрытие вслывающего окна
    else if (e.target.getAttribute('data-micromodal-close') == '') {
        console.log('data-micromodal-close')
        open_micro_modal.classList.remove('is-open')
    }
    // Закрытие вслывающего окна
    else if (e.target.getAttribute('switch-btn')) {
        $(e.target).toggleClass('switch-on');
    }

    //  Смена экранов в настройках
    else if (e.target.getAttribute('data-target')) {
        let elem = e.target.getAttribute('data-target')
        for (el of document.getElementsByClassName('tab-nav__item')) {
            let atributes = el.getAttribute('data-target')
            if (atributes == elem) {
                el.classList.add('is-active')
                document.getElementById(atributes).style.display = 'block'
            } else {
                el.classList.remove('is-active')
                document.getElementById(atributes).style.display = 'none'

            }

        }
    }


    //  Смена экранов в API Keys
    else if (e.target.getAttribute('page-api')) {
        let elem = e.target.getAttribute('page-api')
        for (el of document.querySelectorAll('[page-api-block]')) {
            let atributes = el.getAttribute('id')
            if (atributes == elem) {
                document.getElementById(atributes).style.display = 'block'
            } else {
                document.getElementById(atributes).style.display = 'none'
            }
        }
    }

    //  Копирование текста
    else if (e.target.getAttribute('copy-text')) {
        let elem = document.getElementById(e.target.getAttribute('copy-text'))
        navigator.clipboard.writeText(elem.innerText)

    }//  переход по ссылке
    else if (e.target.getAttribute('to-url')) {
        let url = e.target.getAttribute('to-url')
        let urls;
        if(url.indexOf('http') !== -1) {
            urls = url
        } else {
            urls = location.origin + url
        }
        console.log(urls)
        location.href = urls
    }
    else if (e.target.getAttribute('to-new-url')) {
        let url = e.target.getAttribute('to-new-url')
        let urls;
        if(url.indexOf('http') !== -1) {
            urls = url
        } else {
            urls = location.origin + url
        }
        console.log(urls)
        window.open(urls, '_blank');
    }
    if (e.target.getAttribute('to-send')) {
        let url = e.target.getAttribute('to-send')
        sender(e.target, url, 'POST')
    } // Открытие данных по оплате криптой
    else if (e.target.getAttribute('dmt_uuid')) {

        let elem = document.getElementById('modal-balance-3')
        open_micro_modal = elem
        let mainelem = document.getElementById(e.target.getAttribute('dmt_uuid'))
        console.log(elem)
        console.log(mainelem)
        elem.getElementsByClassName('m-total')[0].innerText = mainelem.getElementsByClassName('d-table__amount-title')[0].innerText
        elem.getElementsByClassName('m-uuid')[0].innerText = e.target.getAttribute('dmt_uuid')
        elem.getElementsByClassName('m-status')[0].innerText = mainelem.getElementsByClassName('d-status')[0].innerText
        if (mainelem.getElementsByClassName('d-status')[0].getAttribute('id_db') != 1) {
            elem.getElementsByClassName('stats')[0].style.display = 'None'
        }
        elem.getElementsByClassName('m-data-start')[0].innerText = mainelem.getElementsByClassName('x-data-create')[0].innerText
        elem.getElementsByClassName('p-to-url')[0].setAttribute('to-url',
            elem.getElementsByClassName('p-to-url')[0].getAttribute('urls').replace('IDS', e.target.getAttribute('dmt_uuid')).replace('STS', '2'))


        elem.classList.add('is-open')
    } else if (e.target.getAttribute('dmtb_uuid')) {
        let elem = document.getElementById('modal-balance-4')
        open_micro_modal = elem
        let mainelem = document.getElementById(e.target.getAttribute('dmtb_uuid'))
        console.log(mainelem)
        elem.getElementsByClassName('m-total')[0].innerText = mainelem.getElementsByClassName('d-table__amount-title')[0].innerText
        elem.getElementsByClassName('m-uuid')[0].innerText = e.target.getAttribute('dmtb_uuid')
        elem.getElementsByClassName('m-status')[0].innerText = mainelem.getElementsByClassName('d-status')[0].innerText
        elem.getElementsByClassName('m-data-start')[0].innerText = mainelem.getElementsByClassName('x-data-create')[0].innerText
        console.log(mainelem.getElementsByClassName('x-data-descriptions')[0].innerText)
        elem.getElementsByClassName('m-descriptions')[0].innerText = mainelem.getElementsByClassName('x-data-descriptions')[0].innerText


        elem.classList.add('is-open')
    } //кнопка удаление
    else if (e.target.getAttribute('delete_tg')) {

        let elem = document.getElementById('modal-remove-tg')
        console.log(e.target.getAttribute('delete_tg'))
        let t = 'Вы действительно хотите удалить аккаунт ' + e.target.getAttribute('id_tg') + '?'
        document.getElementById('ttext').innerText = t
        document.getElementById('tgg').innerText = e.target.getAttribute('id_tg')
        let lc = document.getElementById('buttremtg').getAttribute('to-url') +
            'removetg/' + e.target.getAttribute('delete_tg')
        document.getElementById('buttremtg').setAttribute('to-url', lc)
        open_micro_modal = elem
        elem.classList.add('is-open')
    } else if (e.target.getAttribute('Prodamus')) {
        console.log('works')
    }
});

function set_payment_method(e) {
    if (e.getAttribute('m-balance-change') == 'coin') {
        console.log('coin', e.getAttribute('m-balance-change'))

    } else if (e.getAttribute('m-balance-change') == 'area') {
        {
            console.log('ареа', (e.value))
            for (el of document.getElementsByClassName('AChanger')) {
                console.log('ss', el)
                if (el.classList.value.indexOf(e.value) !== -1) {
                    el.style.display = 'block';
                } else {
                    el.style.display = 'none';
                }
            }
        }
    }
}


function ch_l(e) {
    // console.log(e.value)
    // console.log(location)
    let s = '?'
    for (el of document.getElementsByClassName('SVS')){
        console.log(el.value)
        s += el.value
    }
    lc = location.origin + location.pathname + s
    // console.log(lc)
    location = lc
    // location = location.origin + location.pathname + '?' + this.value;
}


function change_percent(e) {
    url = '/app/settings/' + e.getAttribute('id') + '/set-percent/'
    localize = '/' + location.pathname.split('/')[1]
    u = location.origin + localize + url
    data = {
        'value': e.value
    }
    $.post(u, data, function (data) {
    })
}

function get_transaction() {
    console.log('Create transactions')
    var frame = document.getElementById('Prodamus-payform-overlay_frame').contentWindow
    console.log(frame)
    document.getElementsByName('order_id')[0].value = '412312'
}

var overlay_links = document.getElementsByClassName('Prodamus-startPay');
if (overlay_links) {
    [].forEach.call(overlay_links, function (e, i, a) {
        e.addEventListener("click", function (evt) {
            get_transaction()
        });
    });
}

link = 'https://demo.payform.ru/?do=pay&'