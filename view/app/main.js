const config = {
    type: 'bar',
    data: {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
            label: '# of money spent',
            data: [1500, 2541, 398, 1412, 945, 102, 2103],
            backgroundColor: ['#EFA159','#AE6D0C','#EFA159','#AE6D0C','#EFA159','#AE6D0C','#EFA159']
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
let pageName = {'home': 'home-page', 'users': 'group-page'}

$.get('./api/remittance-finished', {
    user_id: userId,
    group_id: groupId
}, (data) => {
    if(!data){
        $.get('./api/get-personal-money-information', {
            user_id: userId,
            group_id: groupId
        }, (data) => {
            if (data.need_money > 0) {
                $('.remittance-unpaid h2:nth-child(1)').text('目前餘額：' + data.current_balance)
                $('.remittance-unpaid h2:nth-child(2)').text('仍須匯款：' + data.need_money)
                $('.remittance-account h3:nth-child(2)').text(data.account)
                $.get('./api/get-user-info', {
                    user_id: userId
                }, (data2) => {
                    $('.remittance-paid p').text(data2.name)
                })
                $('.remittance-page').transition('slide up')
            }
        })
    }
})

$.get('./api/get-group-money-information', {
    group_id: groupId
}, (data) => {
    $('.main-top-text h1').text(data.current_balance)
    $('.main-top-text h3').text(data.currency)
    $('.home-today-cost p:nth-child(3)').text(data.currency)
})

$.get('./api/get-one-group-information', {
    group_id: groupId
}, (data) => {
    $('.main-top-text p').text(data.group_name)
    $('.remittance-group-name').text(data.group_name)
})

$.get('./api/get-group-near-event', {
    group_id: groupId,
    days: 7
}, (data) => {
    temp = []
    for (let i = 0; i < 7; i++) {
        temp.push(data['day-list'][i]['total'])
    }
    myChart.config.data.datasets[0].data = temp
    myChart.update()
})

let recoredData = []
$.get('./api/get-group-event', {
    amount: 4,
    group_id: groupId
}, (data) => {
    /*
    temp = ''
    for (let i = 0; i < data.length; i++) {
        recoredData.push(data[i].event_id)
        temp += '<div class=".home-recored-event-' + i + '"><h3>' + data[i].title + '</h3><h3>' + data[i].total_money +'</h3>'
        if (data[i].state) {
            temp += '<i class="big check circle outline icon"></i></div>'
        }else {
            temp += '<i class="big times circle outline icon"></i></div>'
        }
    }
    $('.home-recored').html(temp)
    for (let i = 0; i < data.length; i++) {
        if (data[i].state) {
            $('.home-recored div:nth-child(' + (i + 1) +') i').css('color','#B5A24C')
        }else {
            $('.home-recored div:nth-child(' + (i + 1) +') i').css('color','#B54C4C')
        }
    }*/

    for (let i = 0; i < 3; i++) {
        if (data.length > i) {
            recoredData.push(data[i].event_id)
            $('.home-recored div:nth-child(' + (i + 1) +') h3:nth-child(1)').text(data[i].title)
            $('.home-recored div:nth-child(' + (i + 1) +') h3:nth-child(2)').text(data[i].total_money)
            if ((data[i].state && $('.home-recored div:nth-child(' + (i + 1) +') i').hasClass('times')) || (!data[i].state && $('.home-recored div:nth-child(' + (i + 1) +') i').hasClass('check'))) {
                $('.home-recored div:nth-child(' + (i + 1) +') i').toggleClass('times check')
                if (data[i].state) {
                    $('.home-recored div:nth-child(' + (i + 1) +') i').css('color','#B5A24C')
                }else {
                    $('.home-recored div:nth-child(' + (i + 1) +') i').css('color','#B54C4C')
                }
            }
        }else {
            $('.home-recored div:nth-child(' + (i + 1) +')').html('13')
        }
    }
})

/*
for (let i = 0; i < recoredData.length; i++) {
    $('.home-recored div:nth-child(' + i + ')').click(()=>{
        $.get('./api/get-transaction-info', {
            event_id: recoredData[i]
        }, (data) => {
            $('.add-event-money input[name=event-money]').val(data.amount)
            $('.add-event-content input[name=event-name]').val(data.title)
            $('.add-event-content select[name=event-kind]').val(data.type)
            $('.add-event-content input[name=event-memo]').val(data.note)
        })
        ////////////////////////////
        console.log(i)
        $('.add-event-money input[name=event-money]').attr('readonly','readonly')
        $('.add-event-content input[name=event-name]').attr('readonly','readonly')
        $('.add-event-content select[name=event-kind]').attr('disabled', true)
        $('.add-event-content input[name=event-memo]').attr('readonly','readonly')
        $('.add-event-page').transition('fade')
    })
}*/
let splitMode = 'watch'
$('.home-recored div:nth-child(1)').click(()=>{
    $.get('./api/get-transaction-info', {
        event_id: recoredData[0]
    }, (data) => {
        $('.add-event-money input[name=event-money]').val(data.amount)
        $('.add-event-content input[name=event-name]').val(data.title)
        $('.add-event-content select[name=event-kind]').val(data.type)
        $('.add-event-content input[name=event-memo]').val(data.note)
        console.log(data)
        let tempPeople = ''
        let tempRecored = ''
        for (let i = 0; i < data.divider.length; i++) {
            tempPeople += '<div></div>'
            tempRecored += '<div><div></div><h3>' + data.divider[i].nickname  +'</h3><input type="number" placeholder="輸入 %數"></div>'
        }
        $('.split-people').html(tempPeople)
        $('.split-recored').html(tempRecored)
        for (let i = 0; i < data.divider.length; i++) {
            $('.split-recored input:nth-child(3)')[i].value = data.divider[i].input_value
            $('.split-recored input:nth-child(3)')[i].setAttribute('readonly','true')
        }
    })
    $('.add-event-money input[name=event-money]').attr('readonly','readonly')
    $('.add-event-content input[name=event-name]').attr('readonly','readonly')
    $('.add-event-content select[name=event-kind]').attr('disabled', true)
    $('.add-event-content input[name=event-memo]').attr('readonly','readonly')
    $('.add-event-page').transition('fade')
})

$('.remittance-page button').click(() =>{
    if($('.remittance-paid').hasClass('hidden')) {
        $('.remittance-page button').text('開始記帳')
        $('.remittance-unpaid').transition('toggle')
        $('.remittance-paid').transition('toggle')
    }else {
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
            let temp = {'user_id': data[i].user_id, 'value': 0}
            splitDivider.push(temp)
            tempPeople += '<div></div>'
            tempRecored += '<div><div></div><h3>' + data[i].user_name  +'</h3><input type="number" placeholder="輸入 %數"></div>'
        }
        $('.split-people').html(tempPeople)
        $('.split-recored').html(tempRecored)
    })
    $('.add-event-page').transition('fade')
})

$('.add-event-page .close').click(() => {
    if ($('.split-account').hasClass('hidden')) {
        $('.add-event-page').transition('fade')
        if (splitStatus){
            splitStatus = false
            splitDivider = []
            $('.add-event-money input[name=event-money]').val('')
            $('.add-event-content input[name=event-name]').val('')
            $('.add-event-content select[name=event-kind]').val('food')
            $('.add-event-content input[name=event-memo]').val('')
            $('.add-event-money input[name=event-money]').removeAttr('readonly')
            $('.add-event-content input[name=event-name]').removeAttr('readonly')
            $('.add-event-content select[name=event-kind]').attr('disabled', false)
            $('.add-event-content input[name=event-memo]').removeAttr('readonly')
            $('.add-event-content button').text('確定')
            $('.add-event-content button').css('background-color','#EFA159')
        }
    }else {
        $('.split-account').transition('fade')
    }
})

$('.add-event-content .split-people-btn').click(() => {
    if ($('.add-event-content button').text() != '更改'){
        $('.split-account').transition('toggle')
    }
})

$('.split-account button').click(() => {
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
            }else {
                for (let j = 0; j < data.length; j++) {
                    splitDivider[j].value = parseFloat($('.split-recored input:nth-child(3)')[j].value)
                }
                $('.split-account-error-msg').html('')
                $('.split-account').transition('toggle')
                splitStatus = true
                console.log(splitDivider)
            }
        }
    })
})

$('.add-event-content button').click(() => {
    if($('.add-event-content input[name=event-name]').val() === '' || $('.add-event-money input[name=event-money]').val() === '') {
        $('.add-event-content-error-msg').html('請填寫金額及項目名稱！')
    }else if (!splitStatus) {
        $('.add-event-content-error-msg').html('請選擇分帳人及分帳方式！')
    }else {
        console.log(JSON.stringify(splitDivider))
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
            console.log(data)
        })
        $('.add-event-content-error-msg').html('')
        $('.add-event-money input[name=event-money]').attr('readonly','readonly')
        $('.add-event-content input[name=event-name]').attr('readonly','readonly')
        $('.add-event-content select[name=event-kind]').attr('disabled', true)
        $('.add-event-content input[name=event-memo]').attr('readonly','readonly')
        $('.add-event-content button').text('更改')
        $('.add-event-content button').css('background-color','#AE6D0C')
    }
})

$('.main-buttom-banner .home').click(() => {
    $('.main-buttom-banner .' + pageNow).css('color', '#605416')
    $('.' + pageName[pageNow]).transition('toggle')
    pageNow = 'home'
    $('.main-buttom-banner .' + pageNow).css('color', '#fff3e0')
    $('.' + pageName[pageNow]).transition('toggle')

})

$('.main-buttom-banner .users').click(() => {
    $('.main-buttom-banner .' + pageNow).css('color', '#605416')
    $('.' + pageName[pageNow]).transition('toggle')
    pageNow = 'users'
    $('.main-buttom-banner .' + pageNow).css('color', '#fff3e0')
    $('.' + pageName[pageNow]).transition('toggle')
})
