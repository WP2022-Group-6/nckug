const barConfig = {
    type: 'bar',
    data: {
        labels: ['First day', 'Second day', 'Third day', 'Fourth day', 'Fifth day', 'sixth day', 'seventh day'],
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
const barChart = new Chart(document.getElementById('barChart'), barConfig)

const pieConfig = {
    type: 'pie',
    data: {
        labels: ['住宿', '食物', '門票', '交通'],
        datasets: [{
            label: '# of money spent',
            data: [1403, 548, 985, 200],
            backgroundColor: ['#456228', '#798337', '#B5A24C', '#F6BF6A']
        }]
    },
    options: {
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right',
                align: 'start',
                labels: {
                    usePointStyle: true,
                    font: {
                        size: 15,
                        weight: 'bold'
                    }
                }
            }
        }
    }
}
const pieChart = new Chart(document.getElementById('pieChart'), pieConfig)

const urlParams = new URLSearchParams(window.location.search)
let userId = urlParams.get('user-id')
let groupId = urlParams.get('group-id')
let pageNow = 'home'

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
        barChart.barConfig.data.datasets[0].data = temp.reverse()
        barChart.update()
    })
}

let eventId
let splitMode = 'add'
home_record_refresh()
function home_record_refresh() {
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
        $('.home-record').html('')
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
            $('.home-record').append(tempDiv)
            document.querySelectorAll('.home-record div')[i].addEventListener('click', function () {
                eventId = data[i].event_id
                $.get('./api/get-transaction-info', {
                    event_id: data[i].event_id
                }, (data1) => {
                    $('.add-event-money input[name=event-money]').val(data1.amount)
                    $('.add-event-content input[name=event-name]').val(data1.title)
                    $('.add-event-content select[name=event-kind]').val(data1.type)
                    $('.add-event-content input[name=event-memo]').val(data1.note)
                    let tempPeople = ''
                    let temprecord = ''
                    for (let i = 0; i < data1.divider.length; i++) {
                        tempPeople += '<div></div>'
                        temprecord += '<div><div></div><h3>' + data1.divider[i].nickname + '</h3><input type="number" placeholder="輸入 %數"></div>'
                    }
                    $('.split-people').html(tempPeople)
                    $('.split-record').html(temprecord)
                    for (let i = 0; i < data1.divider.length; i++) {
                        $('.split-record input:nth-child(3)')[i].value = data1.divider[i].input_value
                        $('.split-record input:nth-child(3)')[i].setAttribute('readonly', 'true')
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

// 匯款頁面btn
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

// 下方選單btn
let splitStatus = false
let splitMethod = [{method: 'percentage', title: '比例', depiction: '按每人佔比分配', place: '輸入 %數'},
                    {method: 'extra', title: '額外支出', depiction: '扣除每人額外支出後，剩下花費平均分配', place: '額外金額'},
                    {method: 'normal', title: '實際花費', depiction: '輸入每人實際花費金額', place: '實際金額'},
                    {method: 'number_of', title: '份數', depiction: '輸入每人購買的份數', place: '購買份數'}]
let splitMethodNow = 'percentage'
let splitDivider = []
$('.main-buttom-banner .plus').click(() => {
    $.get('./api/get-group-member', {
        group_id: groupId
    }, (data) => {
        let tempPeople = ''
        let temprecord = ''
        for (let i = 0; i < data.length; i++) {
            let temp = { 'user_id': data[i].user_id, 'value': 0 }
            splitDivider.push(temp)
            tempPeople += '<div></div>'
            temprecord += '<div><div></div><h3>' + data[i].user_name + '</h3><input type="number" placeholder="輸入 %數"></div>'
        }
        $('.split-people').html(tempPeople)
        $('.split-record').html(temprecord)
    })
    $('.add-event-page').transition('fade')
})

$('.main-buttom-banner .home').click(() => {
    if (pageNow != 'home') {
        if (pageNow === 'personal') {
            $('.personal-record-page').transition('toggle')
            $('.main-top').transition('toggle')
            $('.home-page').transition('toggle')
        } else if (pageNow === 'chart') {
            $('.chart-bottom-part').transition('toggle')
            $('.home-bottom-part').transition('toggle')
            $('.main-buttom-banner .' + pageNow).css('color', '#605416')
        } else {
            if (pageNow === 'list') {
                $('.main-top').transition('toggle')
                $('.record-page').transition('toggle')
            } else {
                $('.group-page').transition('toggle')
            }
            $('.home-page').transition('toggle')
            $('.main-buttom-banner .' + pageNow).css('color', '#605416')
        }
        pageNow = 'home'
        $('.main-buttom-banner .home').css('color', '#fff3e0')
        home_record_refresh()
        bar_chart_refresh()
        top_text_refresh()
    }
})

$('.main-buttom-banner .chart').click(() => {
    if (pageNow != 'chart') {
        if (pageNow != 'personal') {
            if (pageNow === 'list') {
                $('.home-page').transition('toggle')
                $('.main-top').transition('toggle')
                $('.record-page').transition('toggle')
            } else if (pageNow === 'users') {
                $('.group-page').transition('toggle')
                $('.home-page').transition('toggle')
            }
            $('.main-buttom-banner .' + pageNow).css('color', '#605416')
        } else {
            $('.main-top').transition('toggle')
            $('.personal-record-page').transition('toggle')
            $('.home-page').transition('toggle')
        }
        pageNow = 'chart'
        $('.main-buttom-banner .' + pageNow).css('color', '#fff3e0')
        $('.home-bottom-part').transition('toggle')
        $('.chart-bottom-part').transition('toggle')
        // refresh func尚未實作
    }
})

$('.main-buttom-banner .list').click(() => {
    if (pageNow != 'list') {
        if (pageNow != 'personal') {
            if (pageNow === 'chart') {
                $('.chart-bottom-part').transition('toggle')
                $('.home-bottom-part').transition('toggle')
                $('.home-page').transition('toggle')
            }else if (pageNow === 'home') {
                $('.home-page').transition('toggle')
            }else {
                $('.group-page').transition('toggle')
            }
            $('.main-buttom-banner .' + pageNow).css('color', '#605416')
            $('.main-top').transition('toggle')
        } else {
            $('.personal-record-page').transition('toggle')
        }
        pageNow = 'list'
        $('.main-buttom-banner .' + pageNow).css('color', '#fff3e0')
        $('.record-page').transition('toggle')
        // refresh func尚未實作
    }
})

$('.main-buttom-banner .users').click(() => {
    if (pageNow != 'users') {
        if (pageNow != 'personal') {
            if (pageNow === 'chart') {
                $('.chart-bottom-part').transition('toggle')
                $('.home-bottom-part').transition('toggle')
                $('.home-page').transition('toggle')
            }else if (pageNow === 'home') {
                $('.home-page').transition('toggle')
            }else {
                $('.main-top').transition('toggle')
                $('.record-page').transition('toggle')
            }
            $('.main-buttom-banner .' + pageNow).css('color', '#605416')
        }else {
            $('.main-top').transition('toggle')
            $('.personal-record-page').transition('toggle')
        }
        pageNow = 'users'
        $('.main-buttom-banner .' + pageNow).css('color', '#fff3e0')
        $('.group-page').transition('toggle')
        top_text_refresh()
        group_page_refresh()
    }
})

// 個人頁面相關btn
$('.main-top-text i.circle').click(() => {
    EnterpersonalPage()
})
$('.record-top-text i.circle').click(() => {
    EnterpersonalPage()
})

function EnterpersonalPage() {
    if (pageNow === 'chart') {
        $('.chart-bottom-part').transition('toggle')
        $('.home-bottom-part').transition('toggle')
        $('.home-page').transition('toggle')
        $('.main-top').transition('toggle')
    }else if (pageNow === 'home') {
        $('.home-page').transition('toggle')
        $('.main-top').transition('toggle')
    }else if (pageNow == 'users') {
        $('.group-page').transition('toggle')
        $('.main-top').transition('toggle')
    } else {
        $('.record-page').transition('toggle')
    }
    $('.main-buttom-banner .' + pageNow).css('color', '#605416')
    pageNow = 'personal'
    $('.personal-record-page').transition('toggle')
}

// 群組頁面btn
$('.group-page button').click(() => {
    $('.close-account-page').transition('slide up')
})

// 結算畫面btn
$('.close-account-page i.chevron.left').click(() => {
    $('.close-account-page').transition('slide up')
})

$('.close-review-page .close-account-btn').click(() => {
    $('.close-review-page').transition('toggle')
    $('.close-done-page').transition('toggle')
    $('.close-account-page i.chevron.left').transition('toggle')
})

var closeTransactionTitle = document.querySelectorAll('.close-transaction-title')
visibleNow = -1
closeTransactionTitle.forEach((title, index) => {
    title.addEventListener('click', () => {
        if (visibleNow != index) {
            $('.close-transaction-detail.visible').transition('toggle')
        }
        visibleNow = index
        $('.close-transaction-content .close-transaction-detail:nth-child(' + (2 * (index + 1)) + ')').transition('toggle')
    })
})

$('.close-review-page button').click(() => {
    $('.close-account-page').transition('toggle')
    $('.close-transaction-page').transition('toggle')
})

$('.close-transaction-page button').click(() => {
    $('.close-transaction-page').transition('toggle')
    $('.close-account-page').transition('toggle')
})

// 寄送邀請頁面btn
$('.send-invitation-page .close').click(() => {
    $('.send-invitation-page').transition('slide up')
})

$('.send-invitation-page button').click(() => {
    ////////// 複製連結
})

// 新增帳目頁面btn
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
                if ($('.split-record input:nth-child(3)')[i].value === '') {
                    $('.split-account-error-msg').html('請輸入每個人的分配比例！')
                    NoBlank = false
                    break
                }
            }
            if (NoBlank) {
                let temp = 0
                for (let j = 0; j < data.length; j++) {
                    temp += parseFloat($('.split-record input:nth-child(3)')[j].value)
                }
                if (temp != 100) {
                    $('.split-account-error-msg').html('每個人的比例加總需為100！')
                } else {
                    for (let j = 0; j < data.length; j++) {
                        splitDivider[j].value = parseFloat($('.split-record input:nth-child(3)')[j].value)
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

$('.add-event-comment').click(() => {
    $('.add-event-money').transition('toggle')
    $('.comment-page-top').transition('toggle')
    $('.add-event-content').transition('toggle')
    $('.comment-page').transition('toggle')
    $('.add-event-comment i').toggleClass('list comment')
})

var splitBtn = document.querySelectorAll('.split-account-navbar .split-way')
splitBtn.forEach((button, index) => {
    button.addEventListener('click', () => {
        $('.split-account-navbar :nth-child(' + (index + 1) + ')').css('border', '1.5vw solid #AE6D0C')
        let indexNow = splitMethod.findIndex(object => {
            return object.method === splitMethodNow
        })
        $('.split-account-navbar :nth-child(' + (indexNow + 1) + ')').css('border', '0')
        splitMethodNow = splitMethod[index].method
        $('.split-account-content h2').text(splitMethod[index].title)
        $('.split-content-depiction p').text(splitMethod[index].depiction)
        document.querySelectorAll('.split-record div input').forEach((input) => {
            input.placeholder = splitMethod[index].place
        })
        if (splitMethod[index].method === 'normal') {
            $('.split-content-depiction i').css('display', 'flex')
        } else {
            $('.split-content-depiction i').css('display', 'none')
        }
    })
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
            split_method: splitMethodNow,
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
        home_record_refresh()
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

// 彈出側欄選單
$('.side-menu-block').click(() => {
    $('.side-menu-page').transition('slide right')
})

$('.main-top i.align.justify').click(() => {
    $('.side-menu-page').transition('slide right')
})
$('.record-top-text i.align.justify').click(() => {
    $('.side-menu-page').transition('slide right')
})
$('.personal-top-text i.align.justify').click(() => {
    $('.side-menu-page').transition('slide right')
})


function group_page_refresh() {
    $.get('/api/get-group-member', {
        group_id: groupId
    }, (data) => {
        $('.group-record').html('')
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
            $('.group-record').append(tempDiv)
        }
        let tempDiv = document.createElement('div')
        tempDiv.classList.add('group-invite-others')
        let tempPic = document.createElement('div')
        let tempName = document.createElement('h3')
        tempName.textContent = '邀請其他朋友'
        tempDiv.appendChild(tempPic)
        tempDiv.appendChild(tempName)
        $('.group-record').append(tempDiv)
        document.querySelector('.group-invite-others').addEventListener('click', function () {
            // 尚未接api
            $('.send-invitation-page').transition('slide up')
        })
    })
}
