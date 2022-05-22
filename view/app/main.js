const config = {
    type: 'bar',
    data: {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
            label: '# of money spent',
            data: [1500, 2541, 398, 1412, 945, 102, 2103],
            backgroundColor: ['#EFA159', '#AE6D0C', '#EFA159', '#AE6D0C', '#EFA159', '#AE6D0C', '#EFA159']
        }]
    },
    options: {
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                position: 'right'
            },
            x: {
                grid: {
                    display: false,
                },
                ticks: {
                    display: false
                }
            }
        },
        plugins: {
            legend: {
                display: false
            }
        }
    }
}
const myChart = new Chart(document.getElementById('barChart'), config)

const urlParams = new URLSearchParams(window.location.search)
let userId = urlParams.get('user-id')
let groupId = urlParams.get('group-id')
let pageNow = 'home'
let pageName = { 'home': 'home-page', 'users': 'group-page' }

$.get('./api/get-personal-money-information', {
    user_id: userId,
    group_id: groupId
}, (data) => {
    if (data.need_money > 0) {
        $('.remittance-unpaid h2:nth-child(1)').text('目前餘額：' + data.current_balance)
        $('.remittance-unpaid h2:nth-child(2)').text('仍須匯款：' + data.need_money)
        $('.remittance-account h3:nth-child(2)').text(data.account)
        $.get('/api/get-group-user-info', {
            user_id: userId,
            group_id: groupId
        }, (data2) => {
            $('.remittance-paid p').text(data2.user_name)
        })
        $('.remittance-page').transition('slide up')
    }
})

top_text_refresh()
function top_text_refresh() {
    $.get('./api/get-group-money-information', {
        group_id: groupId
    }, (data) => {
        $('.main-top-text h1').text(data.current_balance)
        $('.main-top-text h3').text(data.currency)
        $('.home-today-cost p:nth-child(3)').text(data.currency)
    })
}

$.get('./api/get-one-group-information', {
    group_id: groupId
}, (data) => {
    $('.main-top-text p').text(data.group_name)
    $('.remittance-group-name').text(data.group_name)
})

bar_chart_refresh()
function bar_chart_refresh() {
    $.get('./api/get-group-near-event', {
        group_id: groupId,
        days: 7
    }, (data) => {
        $('.home-today-cost p:nth-child(2)').text(data.last_day_total)
        temp = []
        for (let i = 0; i < 7; i++) {
            temp.push(data['day-list'][i]['total'])
        }
        myChart.config.data.datasets[0].data = temp.reverse()
        myChart.update()
    })
}

let eventId
let splitMode = 'add'
home_recored_refresh()

function home_recored_refresh() {
    $.get({
        url: './api/get-group-event',
        headers: {
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
    }, {
        amount: 4,
        group_id: groupId
    }, (data) => {
        $('.home-recored').html('')
        for (let i = 0; i < data.length; i++) {
            let tempDiv = document.createElement('div')
            let tempName = document.createElement('h3')
            tempName.textContent = data[i].title
            let tempCost = document.createElement('h3')
            tempCost.textContent = data[i].total_money
            let tempIcon = document.createElement('i')
            if (data[i].state) {
                tempIcon.classList.add('big', 'check', 'circle', 'outline', 'icon')
                tempIcon.style.color = '#B5A24C'
            } else {
                tempIcon.classList.add('big', 'times', 'circle', 'outline', 'icon')
                tempIcon.style.color = '#B54C4C'
            }
            tempDiv.appendChild(tempName)
            tempDiv.appendChild(tempCost)
            tempDiv.appendChild(tempIcon)
            $('.home-recored').append(tempDiv)
            document.querySelectorAll('.home-recored div')[i].addEventListener('click', function () {
                eventId = data[i].event_id
                $.get('./api/get-transaction-info', {
                    event_id: data[i].event_id
                }, (data1) => {
                    $('.add-event-money input[name=event-money]').val(data1.amount)
                    $('.add-event-content input[name=event-name]').val(data1.title)
                    $('.add-event-content select[name=event-kind]').val(data1.type)
                    $('.add-event-content input[name=event-memo]').val(data1.note)
                    let tempPeople = ''
                    let tempRecored = ''
                    for (let i = 0; i < data1.divider.length; i++) {
                        tempPeople += '<div></div>'
                        tempRecored += '<div><div></div><h3>' + data1.divider[i].nickname + '</h3><input type="number" placeholder="輸入 %數"></div>'
                    }
                    $('.split-people').html(tempPeople)
                    $('.split-recored').html(tempRecored)
                    for (let i = 0; i < data1.divider.length; i++) {
                        $('.split-recored input:nth-child(3)')[i].value = data1.divider[i].input_value
                        $('.split-recored input:nth-child(3)')[i].setAttribute('readonly', 'true')
                    }
                    if (data1.payer_id === parseFloat(userId)) {
                        $('.add-event-content .add-event-save').text('更改')
                        $('.add-event-content .add-event-save').css('background-color', '#AE6D0C')
                        $('.add-event-content .add-event-save').attr('disabled', true)
                    } else {
                        $('.add-event-content .add-event-save').transition('toggle')
                        $('.add-event-content .add-event-agreement').transition('toggle')
                        for (let i = 0; i < data1.divider.length; i++) {
                            if (data1.divider[i].user_id === parseFloat(userId)) {
                                if (data1.divider[i].state === true) {
                                    $('.add-event-agreement button:nth-child(1)').transition('toggle')
                                }
                            }
                        }
                    }
                })
                splitMode = 'watch'
                $('.add-event-money input[name=event-money]').attr('readonly', 'readonly')
                $('.add-event-content input[name=event-name]').attr('readonly', 'readonly')
                $('.add-event-content select[name=event-kind]').attr('disabled', true)
                $('.add-event-content input[name=event-memo]').attr('readonly', 'readonly')
                $('.add-event-page').transition('fade')
            })
        }
    })
}

$('.remittance-page button').click(() => {
    if ($('.remittance-paid').hasClass('hidden')) {
        $.get('./api/remittance-finished', {
            user_id: userId,
            group_id: groupId
        })
        $('.remittance-page button').text('開始記帳')
        $('.remittance-unpaid').transition('toggle')
        $('.remittance-paid').transition('toggle')
    } else {
        $('.remittance-page').transition({
            animation: 'slide up',
            onComplete: () => {
                $('.remittance-page button').text('複製帳號')
                $('.remittance-unpaid').transition('toggle')
                $('.remittance-paid').transition('toggle')
            }
        })
    }
})

let splitStatus = false
let splitMethod = 'percentage'
let splitDivider = []
$('.main-buttom-banner .plus').click(() => {
    $.get('./api/get-group-member', {
        group_id: groupId
    }, (data) => {
        let tempPeople = ''
        let tempRecored = ''
        for (let i = 0; i < data.length; i++) {
            let temp = { 'user_id': data[i].user_id, 'value': 0 }
            splitDivider.push(temp)
            tempPeople += '<div></div>'
            tempRecored += '<div><div></div><h3>' + data[i].user_name + '</h3><input type="number" placeholder="輸入 %數"></div>'
        }
        $('.split-people').html(tempPeople)
        $('.split-recored').html(tempRecored)
    })
    $('.add-event-page').transition('fade')
})

$('.add-event-page .close').click(() => {
    if ($('.split-account').hasClass('hidden')) {
        $('.add-event-page').transition('fade')
        if (splitStatus || splitMode === 'watch') {
            splitStatus = false
            splitDivider = []
            splitMode = 'add'
            $('.add-event-content-error-msg').html('')
            $('.add-event-money input[name=event-money]').val('')
            $('.add-event-content input[name=event-name]').val('')
            $('.add-event-content select[name=event-kind]').val('food')
            $('.add-event-content input[name=event-memo]').val('')
            $('.add-event-money input[name=event-money]').removeAttr('readonly')
            $('.add-event-content input[name=event-name]').removeAttr('readonly')
            $('.add-event-content select[name=event-kind]').attr('disabled', false)
            $('.add-event-content input[name=event-memo]').removeAttr('readonly')
            $('.add-event-content .add-event-save').text('儲存')
            $('.add-event-content .add-event-save').css('background-color', '#EFA159')
            $('.add-event-content .add-event-save').attr('disabled', false)
            if ($('.add-event-content .add-event-save').hasClass('hidden')) {
                $('.add-event-content .add-event-save').transition('toggle')
                $('.add-event-content .add-event-agreement').transition('toggle')
            }
            if ($('.add-event-agreement button:nth-child(1)').hasClass('hidden')) {
                $('.add-event-agreement button:nth-child(1)').transition('toggle')
            }
        }
    } else {
        $('.split-account-error-msg').html('')
        $('.split-account').transition('fade')
    }
})

$('.add-event-content .split-people-btn').click(() => {
    if ($('.add-event-content .add-event-save').text() != '更改') {
        $('.split-account').transition('toggle')
    }
})

$('.split-account button').click(() => {
    if (splitMode === 'add') {
        $.get('./api/get-group-member', {
            group_id: groupId
        }, (data) => {
            let NoBlank = true
            for (let i = 0; i < data.length; i++) {
                if ($('.split-recored input:nth-child(3)')[i].value === '') {
                    $('.split-account-error-msg').html('請輸入每個人的分配比例！')
                    NoBlank = false
                    break
                }
            }
            if (NoBlank) {
                let temp = 0
                for (let j = 0; j < data.length; j++) {
                    temp += parseFloat($('.split-recored input:nth-child(3)')[j].value)
                }
                if (temp != 100) {
                    $('.split-account-error-msg').html('每個人的比例加總需為100！')
                } else {
                    for (let j = 0; j < data.length; j++) {
                        splitDivider[j].value = parseFloat($('.split-recored input:nth-child(3)')[j].value)
                    }
                    $('.split-account-error-msg').html('')
                    $('.split-account').transition('toggle')
                    splitStatus = true
                }
            }
        })
    } else {
        $('.split-account').transition('toggle')
    }
})

$('.add-event-content .add-event-save').click(() => {
    if ($('.add-event-content input[name=event-name]').val() === '' || $('.add-event-money input[name=event-money]').val() === '') {
        $('.add-event-content-error-msg').html('請填寫金額及項目名稱！')
    } else if (!splitStatus) {
        $('.add-event-content-error-msg').html('請選擇分帳人及分帳方式！')
    } else {
        $.get('/api/new-transaction', {
            group_id: groupId,
            title: $('.add-event-content input[name=event-name]').val(),
            amount: $('.add-event-money input[name=event-money]').val(),
            type: $('.add-event-content select[name=event-kind]').val(),
            split_method: splitMethod,
            payer_id: userId,
            note: $('.add-event-content input[name=event-memo]').val(),
            picture: '',
            divider: JSON.stringify(splitDivider)
        }, (data) => {
            eventId = data.event_id
        })
        $('.add-event-content-error-msg').html('')
        $('.add-event-money input[name=event-money]').attr('readonly', 'readonly')
        $('.add-event-content input[name=event-name]').attr('readonly', 'readonly')
        $('.add-event-content select[name=event-kind]').attr('disabled', true)
        $('.add-event-content input[name=event-memo]').attr('readonly', 'readonly')
        $('.add-event-content .add-event-save').text('更改')
        $('.add-event-content .add-event-save').css('background-color', '#AE6D0C')
        $('.add-event-content .add-event-save').attr('disabled', true)
        home_recored_refresh()
        bar_chart_refresh()
        top_text_refresh()
    }
})

$('.add-event-agreement button:nth-child(1)').click(() => {
    let temp = { 'type': 'agree', 'content': '' }
    $.get('./api/dialoge', {
        user_id: userId,
        event_id: eventId,
        message: JSON.stringify(temp)
    }, (data) => {
        if (!data) {
            $('.add-event-content-error-msg').html('系統錯誤請稍後再試！')
        } else {
            $('.add-event-content-error-msg').html('')
            $('.add-event-agreement button:nth-child(1)').transition('toggle')
        }
    })
})

$('.main-buttom-banner .home').click(() => {
    $('.main-buttom-banner .' + pageNow).css('color', '#605416')
    $('.' + pageName[pageNow]).transition('toggle')
    pageNow = 'home'
    $('.main-buttom-banner .' + pageNow).css('color', '#fff3e0')
    $('.' + pageName[pageNow]).transition('toggle')
    home_recored_refresh()
    bar_chart_refresh()
    top_text_refresh()
})

$('.main-buttom-banner .users').click(() => {
    $('.main-buttom-banner .' + pageNow).css('color', '#605416')
    $('.' + pageName[pageNow]).transition('toggle')
    pageNow = 'users'
    $('.main-buttom-banner .' + pageNow).css('color', '#fff3e0')
    $('.' + pageName[pageNow]).transition('toggle')
    top_text_refresh()
    group_page_refresh()
})

function group_page_refresh() {
    $.get('/api/get-group-member', {
        group_id: groupId
    }, (data) => {
        $('.group-recored').html('')
        for (let i = 0; i < data.length; i++) {
            let tempDiv = document.createElement('div')
            let tempPic = document.createElement('div')
            let tempName = document.createElement('h3')
            tempName.textContent = data[i].user_name
            let tempCost = document.createElement('h3')
            tempCost.textContent = data[i].balance
            tempDiv.appendChild(tempPic)
            tempDiv.appendChild(tempName)
            tempDiv.appendChild(tempCost)
            $('.group-recored').append(tempDiv)
        }
        let tempDiv = document.createElement('div')
        tempDiv.classList.add('group-invite-others')
        let tempPic = document.createElement('div')
        let tempName = document.createElement('h3')
        tempName.textContent = '邀請其他朋友'
        tempDiv.appendChild(tempPic)
        tempDiv.appendChild(tempName)
        $('.group-recored').append(tempDiv)
    })
}
