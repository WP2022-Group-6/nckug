$(document).ready(() => {
    var url = 'http://127.0.0.1'
    var port = '5000'
    var socket = io.connect(url + ':' + port)
    socket.on('update', function () {
        console.log('update')
        top_update()
    })
})

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
let groupId = urlParams.get('group-id')
let pageNow = 'home'
$.ajaxSetup({ cache: false })

// 取得userId
let userId
$.get('./api/user/get-user-info', (data) => {
    userId = data.id
})

// 確認是否已匯款
$.get('./api/group/get-user-info', {
    group_id: groupId
}, (data) => {
    if (data.need_money > 0) {
        $('.remittance-unpaid h2:nth-child(1)').text('目前餘額：' + data.balance)
        $('.remittance-unpaid h2:nth-child(2)').text('仍須匯款：' + data.need_money)
        $('.remittance-account h3:nth-child(2)').text(data.account)
        $('.remittance-paid p').text(data.nickname)
        $('.remittance-page').transition('slide up')
    }
})

// 更新上方資訊欄
top_text_refresh()
function top_text_refresh() {
    $.get('./api/group/get-group-info', {
        group_id: groupId
    }, (data) => {
        $('.main-top-text p').text(data.group_name)
        $('.remittance-group-name').text(data.group_name)
        $('.main-top-text h1').text(data.balance)
        $('.main-top-text h3').text(data.currency)
        $('.home-today-cost p:nth-child(3)').text(data.currency)
    })
}

// 更新長條圖
bar_chart_refresh()
function bar_chart_refresh() {
    $.get('./api/transaction/get-group-transaction', {
        group_id: groupId,
        days: 7
    }, (data) => {
        $('.home-today-cost p:nth-child(2)').text(data[6].total)
        temp = []
        for (let i = 0; i < 7; i++) {
            temp.push(data[i]['total'])
        }
        barChart.config.data.datasets[0].data = temp
        barChart.update()
    })
}

// 更新圓餅圖
pie_chart_refresh()
function pie_chart_refresh() {
    $.get('./api/transaction/get-transaction-type', {
        group_id: groupId
    }, (data) => {
        tempName = []
        tempMoney = []
        for (let i = 0; i < Object.keys(data).length; i++) {
            tempName.push(Object.keys(data)[i])
            tempMoney.push(data[Object.keys(data)[i]])
        }
        pieChart.config.data.labels = tempName
        pieChart.config.data.datasets[0].data = tempMoney
        pieChart.update()
    })
}

// 更新帳目頁面
function record_record_refresh() {
    $.get('./api/transaction/get-group-transaction', {
        group_id: groupId
    }, (data) => {
        $('.record-page .record-record').html('')
        let number = 0
        let nonagreed = 0
        for (let i = 0; i < data.length; i++) {
            let tempDate = document.createElement('p')
            tempDate.textContent = data[i].date
            $('.record-page .record-record').append(tempDate)
            for (let j = 0; j < data[i].transactions.length; j++) {
                let tempDiv = document.createElement('div')
                let tempName = document.createElement('h3')
                tempName.textContent = data[i].transactions[j].title
                let tempCost = document.createElement('h3')
                tempCost.textContent = data[i].transactions[j].total_money
                let tempIcon = document.createElement('i')
                if (data[i].transactions[j].state) {
                    tempIcon.classList.add('big', 'check', 'circle', 'outline', 'icon')
                    tempIcon.style.color = '#B5A24C'
                } else {
                    tempIcon.classList.add('big', 'times', 'circle', 'outline', 'icon')
                    tempIcon.style.color = '#B54C4C'
                    nonagreed++
                }
                tempDiv.appendChild(tempName)
                tempDiv.appendChild(tempCost)
                tempDiv.appendChild(tempIcon)
                $('.record-page .record-record').append(tempDiv)
                number += 1
                record_add_click_func('.record-page .record-record div', number, data[i].transactions[j].transaction_id)
                $('.record-top-text h3').text('目前有' + nonagreed + '筆待同意帳目')
            }
        }
    })
}

// 主畫面下方近期紀錄更新
let transactionId
let splitMode = 'add'
home_record_refresh()
function home_record_refresh() {
    $.get('./api/transaction/get-group-transaction', {
        amount: 4,
        group_id: groupId
    }, (data) => {
        $('.home-record').html('')
        let number = 0
        for (let i = 0; i < data.length; i++) {
            for (let j = 0; j < data[i].transactions.length; j++) {
                let tempDiv = document.createElement('div')
                let tempName = document.createElement('h3')
                tempName.textContent = data[i].transactions[j].title
                let tempCost = document.createElement('h3')
                tempCost.textContent = data[i].transactions[j].total_money
                let tempIcon = document.createElement('i')
                if (data[i].transactions[j].state) {
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
                number += 1
                record_add_click_func('.home-record div', number, data[i].transactions[j].transaction_id)
            }
        }
    })
}

function record_add_click_func(divName, number, transaction) {
    document.querySelectorAll(divName)[number - 1].addEventListener('click', function () {
        $.get('./api/transaction/get-info', {
            transaction_id: transaction
        }, (data1) => {
            splitDivider = []
            paidID = data1.payer_id
            transactionId = transaction
            $('.paid-record').html('')
            $('.add-event-money input[name=event-money]').val(data1.amount)
            $('.add-event-content input[name=event-name]').val(data1.title)
            $('.add-event-content select[name=event-kind]').val(data1.type)
            $('.add-event-content input[name=event-memo]').val(data1.note)
            let tempPeople = ''
            let temprecord = ''
            for (let i = 0; i < data1.divider.length; i++) {
                splitDivider.push({ 'user_id': data1.divider[i].user_id, 'value': data1.divider[i].input_value })
                tempPeople += '<div></div>'
                temprecord += '<div><div></div><h3>' + data1.divider[i].nickname + '</h3><input type="number" placeholder="實際金額"></div>'
                let tempDiv = document.createElement('div')
                tempDiv.classList.add('paid-select')
                let tempPic = document.createElement('div')
                if (data1.divider[i].user_id === paidID) {
                    tempPic.style.border = '1.1vw solid #AE6D0C'
                }
                let tempH3 = document.createElement('h3')
                tempH3.textContent = data1.divider[i].nickname
                tempDiv.appendChild(tempPic)
                tempDiv.appendChild(tempH3)
                $('.paid-record').append(tempDiv)
                document.querySelectorAll('.paid-select')[i].addEventListener('click', () => {
                    if ($('.add-event-content .add-event-save').text() != '更改' && paidID === userId) {
                        if (paidID != data1.divider[i].user_id) {
                            for (let j = 0; j < splitDivider.length; j ++) {
                                if (paidID === splitDivider[j].user_id) {
                                    document.querySelectorAll('.paid-select div')[j].style.border = '1.1vw solid #EFA159'
                                    console.log(document.querySelectorAll('.paid-select div'))
                                }
                            }
                        }
                        paidID = data1.divider[i].user_id
                        document.querySelectorAll('.paid-select div')[i].style.border = '1.1vw solid #AE6D0C'
                    }
                })
            }
            $('.split-people').html(tempPeople)
            $('.split-record').html(temprecord)
            for (let i = 0; i < data1.divider.length; i++) {
                $('.split-record input:nth-child(3)')[i].value = data1.divider[i].amount
                $('.split-record input:nth-child(3)')[i].setAttribute('readonly', 'true')
            }
            if (paidID === userId && !data1.state) {
                $('.add-event-content .add-event-save').text('更改')
                $('.add-event-content .add-event-save').css('background-color', '#AE6D0C')
            } else {
                $('.add-event-content .add-event-save').css('display', 'none')
            }
            if(data1.state) {
                $('.add-event-agreement').css('display', 'none')
            } else {
                $('.add-event-agreement').css('display', 'inline-flex')
                for (let i = 0; i < data1.divider.length; i++) {
                    if (data1.divider[i].user_id === userId) {
                        if (data1.divider[i].state === true) {
                            $('.add-event-agreement button:nth-child(1)').css('display', 'none')
                        }
                    }
                }
            }
            // 更新討論頁面
            $('.comment-content').html('')
            let tempComment = ''
            for (let i = data1.message_list.length - 1; i >= 0; i--) {
                tempComment += '<div class="each-comment-space"><div></div><div><p>' + data1.message_list[i].user_name + '</p><p>' + data1.message_list[i].message + '</p></div></div>'
            }
            $('.comment-content').html(tempComment)
            $('.comment-page-top div h3:nth-child(1)').text(data1.title)
            $('.comment-page-top div h3:nth-child(2)').text(data1.amount)
        })
        splitMode = 'watch'
        $('.add-event-money input[name=event-money]').attr('readonly', 'readonly')
        $('.add-event-content input[name=event-name]').attr('readonly', 'readonly')
        $('.add-event-content select[name=event-kind]').attr('disabled', true)
        $('.add-event-content input[name=event-memo]').attr('readonly', 'readonly')
        $('.add-event-comment').css('display', 'flex')
        $('.split-account-navbar').css('display', 'none')
        $('.add-event-page').transition('fade')
        splitStatus = true
    })
}

// 匯款頁面btn
$('.remittance-page button').click(() => {
    if ($('.remittance-paid').hasClass('hidden')) {
        $.get('./api/group/remittance-finished', {
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
    top_text_refresh()
})

// 下方選單btn
let splitStatus = false
let splitMethod = [{method: 'percentage', title: '比例', depiction: '按每人佔比分配', place: '輸入 %數'},
                    {method: 'extra', title: '額外支出', depiction: '扣除每人額外支出後，剩下花費平均分配', place: '額外金額'},
                    {method: 'normal', title: '實際花費', depiction: '輸入每人實際花費金額', place: '實際金額'},
                    {method: 'number_of', title: '份數', depiction: '輸入每人購買的份數', place: '購買份數'}]
let splitMethodNow = 'percentage'
let splitDivider = []
let paidID
$('.main-buttom-banner .plus').click(() => {
    $.get('./api/group/get-group-info', {
        group_id: groupId
    }, (data) => {
        let tempPeople = ''
        let temprecord = ''
        paidID = userId
        $('.paid-record').html('')
        for (let i = 0; i < data.member.length; i++) {
            let temp = { 'user_id': data.member[i].user_id, 'value': 0 }
            splitDivider.push(temp)
            tempPeople += '<div></div>'
            temprecord += '<div><div></div><h3>' + data.member[i].nickname + '</h3><input type="number" placeholder="輸入 %數"></div>'
            let tempDiv = document.createElement('div')
            tempDiv.classList.add('paid-select')
            let tempPic = document.createElement('div')
            if (data.member[i].user_id === paidID) {
                tempPic.style.border = '1.1vw solid #AE6D0C'
            }
            let tempH3 = document.createElement('h3')
            tempH3.textContent = data.member[i].nickname
            tempDiv.appendChild(tempPic)
            tempDiv.appendChild(tempH3)
            console.log(tempDiv)
            $('.paid-record').append(tempDiv)
            $('.add-event-agreement').css('display', 'none')
            document.querySelectorAll('.paid-select')[i].addEventListener('click', () => {
                if ($('.add-event-content .add-event-save').text() != '更改') {
                    if (paidID != data.member[i].user_id) {
                        for (let j = 0; j < splitDivider.length; j ++) {
                            if (paidID === splitDivider[j].user_id) {
                                document.querySelectorAll('.paid-select div')[j].style.border = '1.1vw solid #EFA159'
                                console.log(document.querySelectorAll('.paid-select div'))
                            }
                        }
                    }
                    paidID = data.member[i].user_id
                    document.querySelectorAll('.paid-select div')[i].style.border = '1.1vw solid #AE6D0C'
                }
            })
        }
        $('.split-people').html(tempPeople)
        $('.split-record').html(temprecord)
    })
    $('.add-event-page').transition('fade')
    $('.add-event-comment').css('display', 'none')
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
        bar_chart_refresh()
        pie_chart_refresh()
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
        record_record_refresh()
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
    $.get('./api/group/get-group-info', {
        group_id: groupId
    }, (data) => {
        $('.close-account-page p:nth-child(5)').text(data.group_name)
        $('.close-review-page button p:nth-child(2)').text(data.balance)
        for (let i = 0; i < data.member.length; i++) {
            if (data.member[i].user_id === userId) {
                $('.close-account-page p:nth-child(6)').text(data.member[i].nickname)
                break
            }
        }
    })
    $('.close-account-page').transition('slide up')
})

$('.close-review-page .close-account-btn').click(() => {
    $('.close-review-page').transition('toggle')
    $('.close-done-page').transition('toggle')
    $('.close-account-page i.chevron.left').transition('toggle')
})

let visibleNow = -1
$('.close-review-page button').click(() => {
    $('.close-account-page').transition('toggle')
    let transactionID = []
    $.get('./api/transaction/get-group-transaction', {
        group_id: groupId
    }, (data) => {
        for (let i = 0; i < data.length; i++) {
            for (let j = 0; j < data[i].transactions.length; j++) {
                console.log(data[i].transactions[j].transaction_id)
                transactionID.push(data[i].transactions[j].transaction_id)
            }
        }
        console.log(transactionID)
        $('.close-transaction-content').html('')
        for (let i = 0; i < document.querySelectorAll('.close-transaction-title').length; i++) {
            document.querySelectorAll('.close-transaction-title')[i].removeEventListener('click', () => {
                if (visibleNow != i) {
                    $('.close-transaction-detail.visible').transition('toggle')
                }
                visibleNow = i
                $('.close-transaction-content .close-transaction-detail:nth-child(' + (2 * (i + 1)) + ')').transition('toggle')
            })
        }
        for (let i = 0; i < transactionID.length; i++) {
            $.get('./api/transaction/get-info', {
                transaction_id: transactionID[i],
                amount: 0
            }, (data) => {
                let tempFirstDiv = document.createElement('div')
                tempFirstDiv.classList.add('close-transaction-title')
                let tempTitle = document.createElement('h3')
                tempTitle.textContent = data.title
                let tempMoney = document.createElement('h3')
                tempMoney.textContent = data.amount
                tempFirstDiv.appendChild(tempTitle)
                tempFirstDiv.appendChild(tempMoney)
                $('.close-transaction-content').append(tempFirstDiv)
                let tempSecondDiv = document.createElement('div')
                tempSecondDiv.classList.add('close-transaction-detail', 'transition', 'hidden')

                let tempDiv1 = document.createElement('div')
                let tempDiv11 = document.createElement('div')
                let tempDiv11P1 = document.createElement('p')
                tempDiv11P1.textContent = '日期'
                let tempDiv11P2 = document.createElement('p')
                tempDiv11P2.textContent = data.date.slice(5)
                tempDiv11.appendChild(tempDiv11P1)
                tempDiv11.appendChild(tempDiv11P2)
                let tempDiv12 = document.createElement('div')
                let tempDiv12P1 = document.createElement('p')
                tempDiv12P1.textContent = '種類'
                let tempDiv12P2 = document.createElement('p')
                tempDiv12P2.textContent = data.type
                tempDiv12.appendChild(tempDiv12P1)
                tempDiv12.appendChild(tempDiv12P2)
                tempDiv1.appendChild(tempDiv11)
                tempDiv1.appendChild(tempDiv12)

                let tempDiv2 = document.createElement('div')
                let tempDiv21 = document.createElement('div')
                let tempDiv21P1 = document.createElement('p')
                tempDiv21P1.textContent = '名稱'
                let tempDiv21P2 = document.createElement('p')
                tempDiv21P2.textContent = data.title
                tempDiv21.appendChild(tempDiv21P1)
                tempDiv21.appendChild(tempDiv21P2)
                let tempDiv22 = document.createElement('div')
                let tempDiv22P1 = document.createElement('p')
                tempDiv22P1.textContent = '金額'
                let tempDiv22P2 = document.createElement('p')
                tempDiv22P2.textContent = data.amount
                tempDiv22.appendChild(tempDiv22P1)
                tempDiv22.appendChild(tempDiv22P2)
                tempDiv2.appendChild(tempDiv21)
                tempDiv2.appendChild(tempDiv22)

                let tempDiv3 = document.createElement('div')
                let tempDiv3P1 = document.createElement('p')
                tempDiv3P1.textContent = '備註'
                let tempDiv3P2 = document.createElement('p')
                tempDiv3P2.textContent = data.note
                tempDiv3.appendChild(tempDiv3P1)
                tempDiv3.appendChild(tempDiv3P2)

                tempSecondDiv.appendChild(tempDiv1)
                tempSecondDiv.appendChild(tempDiv2)
                tempSecondDiv.appendChild(tempDiv3)
                $('.close-transaction-content').append(tempSecondDiv)
                // 加上點擊展開功能
                document.querySelectorAll('.close-transaction-title')[i].addEventListener('click', () => {
                    if (visibleNow != i) {
                        $('.close-transaction-detail.visible').transition('toggle')
                    }
                    visibleNow = i
                    $('.close-transaction-content .close-transaction-detail:nth-child(' + (2 * (i + 1)) + ')').transition('toggle')
                })
            })
        }
    })
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

let invite_text = '邀請您加入 Team-Debit 的團隊分帳群組「」，請前往【URL】登入系統後以群組代碼【】及驗證碼【】加入我們！'
$('.send-invitation-page button').click(() => {
    ////////// 複製連結
    const el = document.createElement('textarea')
    el.value = invite_text
    document.body.appendChild(el)
    el.select()
    document.execCommand('copy')
    document.body.removeChild(el)
})

// 新增帳目頁面btn
$('.add-event-page .close').click(() => {
    if ($('.split-account').hasClass('hidden') && $('.paid-account').hasClass('hidden')) {
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
            $('.add-event-comment').css('display', 'none')
            $('.split-account-navbar').css('display', 'flex')
            $('.add-event-content .add-event-save').css('display', 'block')
            $('.add-event-agreement').css('display', 'inline-flex')
            $('.add-event-agreement button:nth-child(1)').css('display', 'block')
            if($('.add-event-comment i').hasClass('list')) {
                $('.add-event-money').transition('toggle')
                $('.comment-page-top').transition('toggle')
                $('.add-event-content').transition('toggle')
                $('.comment-page').transition('toggle')
                $('.add-event-comment i').toggleClass('list comment')
            }
        }
    } else if (!$('.paid-account').hasClass('hidden')) {
        $('.paid-account-error-msg').html('')
        $('.paid-account').transition('fade')
    } else {
        $('.split-account-error-msg').html('')
        $('.split-account').transition('fade')
    }
})

$('.add-event-content .split-people-btn').click(() => {
    $('.split-account').transition('toggle')
})

$('.add-event-content .paid-people-btn').click(() => {
    $('.paid-account').transition('toggle')
})

$('.split-account button').click(() => {
    if (splitMode === 'add') {
        $.get('./api/group/get-group-info', {
            group_id: groupId
        }, (data) => {
            let NoBlank = true
            for (let i = 0; i < data.member.length; i++) {
                if ($('.split-record input:nth-child(3)')[i].value === '') {
                    $('.split-account-error-msg').html('請輸入每個人的分配比例！')
                    NoBlank = false
                    break
                }
            }
            if (NoBlank) {
                let temp = 0
                for (let j = 0; j < data.member.length; j++) {
                    temp += parseFloat($('.split-record input:nth-child(3)')[j].value)
                }
                if (splitMethodNow === 'percentage' && temp != 100) {
                    $('.split-account-error-msg').html('每個人的比例加總需為100！')
                } else if (splitMethodNow === 'extra' && ($('.add-event-money input[name=event-money]').val() === '' || temp > $('.add-event-money input[name=event-money]').val())) {
                    if ($('.add-event-money input[name=event-money]').val() === '') {
                        $('.split-account-error-msg').html('請先填寫總金額！')
                    } else if (temp > $('.add-event-money input[name=event-money]').val()) {
                        $('.split-account-error-msg').html('額外支出不得大於總金額！')
                    }
                } else if (splitMethodNow === 'normal' && temp != $('.add-event-money input[name=event-money]').val()) {
                        $('.split-account-error-msg').html('分配之金額與總金額不符！')
                } else {
                    for (let j = 0; j < data.member.length; j++) {
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

$('.paid-account button').click(() => {
    $('.paid-account').transition('toggle')
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
    if ($('.add-event-content .add-event-save').text() === '儲存') {
        add_and_change_event('add')
    } else if ($('.add-event-content .add-event-save').text() === '更改') {
        $('.add-event-money input[name=event-money]').removeAttr('readonly')
        $('.add-event-content input[name=event-name]').removeAttr('readonly')
        $('.add-event-content select[name=event-kind]').attr('disabled', false)
        $('.add-event-content input[name=event-memo]').removeAttr('readonly')
        $('.add-event-content .add-event-save').text('儲存更改')
        $('.split-account-navbar').css('display', 'flex')
        $('.add-event-comment').css('display', 'none')
    } else {
        add_and_change_event('change')
    }
})

function add_and_change_event(status) {
    if ($('.add-event-content input[name=event-name]').val() === '' || $('.add-event-money input[name=event-money]').val() === '') {
        $('.add-event-content-error-msg').html('請填寫金額及項目名稱！')
    } else if (!splitStatus) {
        $('.add-event-content-error-msg').html('請選擇分帳人及分帳方式！')
    } else {
        if (status === 'add') {
            $.post('./api/transaction/set-transaction', {
                group_id: groupId,
                title: $('.add-event-content input[name=event-name]').val(),
                amount: $('.add-event-money input[name=event-money]').val(),
                type: $('.add-event-content select[name=event-kind]').val(),
                split_method: splitMethodNow,
                payer_id: paidID,
                note: $('.add-event-content input[name=event-memo]').val(),
                picture: '',
                divider: JSON.stringify(splitDivider)
            }, (data) => {
                transactionId = data.transaction_id
                home_record_refresh()
                bar_chart_refresh()
                top_text_refresh()
            })
        } else {
            $.post('./api/transaction/set-transaction', {
                transaction_id: transactionId,
                group_id: groupId,
                title: $('.add-event-content input[name=event-name]').val(),
                amount: $('.add-event-money input[name=event-money]').val(),
                type: $('.add-event-content select[name=event-kind]').val(),
                split_method: splitMethodNow,
                payer_id: paidID,
                note: $('.add-event-content input[name=event-memo]').val(),
                picture: '',
                divider: JSON.stringify(splitDivider)
            }, (data) => {
                transactionId = data.transaction_id
                home_record_refresh()
                bar_chart_refresh()
                top_text_refresh()
            })
        }
        $('.add-event-content-error-msg').html('')
        $('.add-event-money input[name=event-money]').attr('readonly', 'readonly')
        $('.add-event-content input[name=event-name]').attr('readonly', 'readonly')
        $('.add-event-content select[name=event-kind]').attr('disabled', true)
        $('.add-event-content input[name=event-memo]').attr('readonly', 'readonly')
        $('.add-event-content .add-event-save').text('更改')
        $('.add-event-content .add-event-save').css('background-color', '#AE6D0C')
        $('.split-account-navbar').css('display', 'none')
        $('.add-event-comment').css('display', 'flex')
        $('.comment-content').html('')
    }
}

// 帳目同意不同意
$('.add-event-agreement button:nth-child(1)').click(() => {
    let temp = { 'type': 'agree', 'content': '' }
    $.post('/api/transaction/new-message', {
        transaction_id: transactionId,
        message: JSON.stringify(temp)
    }, (data) => {
        if (!data) {
            $('.add-event-content-error-msg').html('系統錯誤請稍後再試！')
        } else {
            $('.add-event-content-error-msg').html('')
            $('.add-event-agreement button:nth-child(1)').css('display', 'none')
        }
    })
})

$('.add-event-agreement button:nth-child(2)').click(() => {
    $.get('/api/transaction/get-info', {
        transaction_id: transactionId,
        amount: 0
    }, (data) => {
        $('.denial-reason-page input[name=event-name]').val(data.title)
    })
    $('.add-event-comment').css('display', 'none')
    $('.denial-reason-page').transition('toggle')
})

$('.denial-container h3:nth-child(1)').click(() => {
    let temp = { 'type': 'disagree', 'content':  '不同意原因：' + $('.denial-container h3:nth-child(1)').text()}
    agreement_add(temp)
})

$('.denial-container h3:nth-child(2)').click(() => {
    let temp = { 'type': 'disagree', 'content':  '不同意原因：' + $('.denial-container h3:nth-child(2)').text()}
    agreement_add(temp)
})

$('.denial-container h3:nth-child(3)').click(() => {
    let temp = { 'type': 'disagree', 'content':  '不同意原因：' + $('.denial-container h3:nth-child(3)').text()}
    agreement_add(temp)
})

function agreement_add(temp) {
    $.post('/api/transaction/new-message', {
        transaction_id: transactionId,
        message: JSON.stringify(temp)
    }, (data) => {
        if (!data) {
            $('.add-event-content-error-msg').html('系統錯誤請稍後再試！')
        } else {
            $('.add-event-content-error-msg').html('')
            $('.add-event-agreement button:nth-child(1)').css('display', 'block')
            $('.add-event-comment').css('display', 'flex')
            $('.denial-reason-page').transition('toggle')
            $.get('/api/group/get-user-info', {
                group_id: groupId
            }, (data1) => {
                let tempComment = '<div class="each-comment-space"><div></div><div><p>' + data1.nickname + '</p><p>' + temp.content + '</p></div></div>'
                $('.comment-content').prepend(tempComment)
            })
            top_update()
        }
    })
}

// 帳目討論頁面btn
$('.comment-input input:nth-child(3)').click(() => {
    if ($('.comment-input input:nth-child(2)').val() != '') {
        $.post('/api/transaction/new-message', {
            transaction_id: transactionId,
            message: JSON.stringify({'type': 'message', 'content': $('.comment-input input:nth-child(2)').val()})
        }, (data) => {
            if (data) {
                $.get('/api/group/get-user-info', {
                    group_id: groupId
                }, (data1) => {
                    let tempComment = '<div class="each-comment-space"><div></div><div><p>' + data1.nickname + '</p><p>' + $('.comment-input input:nth-child(2)').val() + '</p></div></div>'
                    $('.comment-content').prepend(tempComment)
                    $('.comment-input input:nth-child(2)').val('')
                })
                top_update()
            }
        })
    }
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
    $.get('./api/group/get-group-info', {
        group_id: groupId
    }, (data) => {
        $('.group-record').html('')
        for (let i = 0; i < data.member.length; i++) {
            let tempDiv = document.createElement('div')
            let tempPic = document.createElement('div')
            let tempName = document.createElement('h3')
            tempName.textContent = data.member[i].nickname
            let tempCost = document.createElement('h3')
            tempCost.textContent = data.member[i].balance
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
            $('.send-invitation-page .invitation-group-name').text(data.group_name)
            $('.send-invitation-page div:nth-child(5) h3:nth-child(2)').text(data.invite_code)
            $('.send-invitation-page div:nth-child(5) h3:nth-child(4)').text(data.verify_code)
            invite_text = '邀請您加入 Team-Debit 的團隊分帳群組「' + data.group_name + '」，請前往 Team-Debit 登入系統後以群組代碼【' + data.invite_code + '】及驗證碼【' + data.verify_code + '】加入我們！'
            $('.send-invitation-page').transition('slide up')
        })
        if (data.owner_id === userId) {
            $('.group-page button').css('display', 'block')
        } else {
            $('.group-page button').css('display', 'none')
        }
    })
}

function comment_content_update() {
    $.get('./api/transaction/get-info', {
        transaction_id: transactionId
    }, (data1) => {
        $('.comment-content').html('')
        let tempComment = ''
        for (let i = data1.message_list.length - 1; i >= 0; i--) {
            tempComment += '<div class="each-comment-space"><div></div><div><p>' + data1.message_list[i].user_name + '</p><p>' + data1.message_list[i].message + '</p></div></div>'
        }
        $('.comment-content').html(tempComment)
    })
}

function top_update() {
    top_text_refresh()
    bar_chart_refresh()
    pie_chart_refresh()
    home_record_refresh()
    comment_content_update()
}

$('.side-menu-choose-group h3').click(() => {
    window.location = "./forum.html?page=group-chosing-page" + "&group-id=" + groupId
})

$('.side-menu-group-setting h3').click(() => {
    window.location = "./forum.html?page=group-setting-page" + "&group-id=" + groupId
})

$('.side-menu-schedule h3:nth-child(2)').click(() => {
    window.location = "./forum.html?page=schedule-group-page" + "&group-id=" + groupId
})

$('.side-menu-schedule h3:nth-child(3)').click(() => {
    window.location = "./forum.html?page=forum-main-page" + "&group-id=" + groupId
})

$('.side-menu-personal-setting h3:nth-child(3)').click(() => {
    window.location = "./forum.html?page=personal-setting-page" + "&group-id=" + groupId
})
