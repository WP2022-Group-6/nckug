let classArr = ['img1', 'img2', 'img3', 'img-none', 'img-none']
let groupNames = []
$(document).ready(() => {
    var socket = io.connect(window.location.hostname)
})

const urlParams = new URLSearchParams(window.location.search)
let select = urlParams.get('select')
if (select === "True") {
    $.get('./api/user/get-user-info', (data) => {
        let temp = ''
        groupNames = []
        classArr = []
        for (let i = 0; i < data.group.length; i++) {
            if (i < 3) {
                if (data.group[i].picture === '') {
                    temp += '<li class="img' + (i + 1) + '"></li>'
                }
                else {
                    temp += '<li class="img' + (i + 1) + '"><img src="' + data.group[i].picture + '"></li>'
                }
                classArr.push('img' + (i + 1))
            }
            else {
                if (data.group[i].picture === '') {
                    temp += '<li class="img-none"><img src="' + data.group[i].picture + '"></li>'
                } else {
                    temp += '<li class="img-none"></li>'
                }
                classArr.push('img-none')
            }
            let group = {'group_name': data.group[i].group_name, 'group_id': data.group[i].group_id}
            groupNames.push(group)
        }
        // 新增討論區選項
        if (groupNames.length < 3) {
            temp += '<li class="img' + (groupNames.length + 1) + '"></li>'
            classArr.push('img' + (groupNames.length + 1))
        } else {
            temp += '<li class="img-none"></li>'
            classArr.push('img-none')
        }
        groupNames.push({'group_name': '討論區', 'group_id': 0})
        // 處理不足3個
        if (groupNames.length === 1) {
            temp += '<li class="img2"></li><li class="img3"></li>'
            classArr.push('img2')
            classArr.push('img3')
            /////////////////////////////////////改道這!!!
            groupNames.push({'group_name': '討論區', 'group_id': 0})
            groupNames.push({'group_name': '討論區', 'group_id': 0})
        } else if (groupNames.length === 2) {
            temp += '<li class="img3"></li><li class="img-none"></li>'
            classArr.push('img3')
            classArr.push('img-none')
            groupNames.push(groupNames[0])
            groupNames.push({'group_name': '討論區', 'group_id': 0})
        }
        $('.choose-group-page ul.imgbox').html(temp)
        $('.choose-group-page .choose-group-name').text(groupNames[1].group_name)
        if($('.choose-group-page .choose-group-name').text() === '討論區') {
            $('.choose-group-page .choose-group-enter').text('進入討論區')
        }
    })
    $('.choose-group-page').transition('slide up')
}

// 初始頁面btn
$('.entrance-btn button:nth-child(1)').click((event) => {
    event.preventDefault()
    $('.login-page').transition('slide up')
    $('.entrance-title').css('transform', 'translateY(-8vh)')
})

$('.entrance-btn button:nth-child(3)').click((event) => {
    event.preventDefault()
    $('.sign-up-page').transition('slide up')
    $('.entrance-title').css('transform', 'translateY(-15vh)')
})

// 登入頁面btn
$('.login-page i').click((event) => {
    event.preventDefault()
    $('.login-page').transition('slide up')
    $('.entrance-title').css('transform', 'none')
    $('.login-error-msg').html('')
    $('.login-page input[name=email]').val('')
    $('.login-page input[name=pwd]').val('')
})

$('.login-page button').click((event) => {
    event.preventDefault()
    if ($('.login-page input[name=email]').val() === '' || $('.login-page input[name=pwd]').val() === '') {
        $('.login-error-msg').html('Please Enter Your Email And Password.')
    } else {
        $('.login-error-msg').html('')
        $.post('./api/auth/login', {
            email: $('.login-page input[name=email]').val(),
            password: $('.login-page input[name=pwd]').val()
        }, (data) => {
            if (data === 'failed') {
                $('.login-error-msg').html('Error Email or Password.')
            }
            else {
                $('.login-page').transition('slide up')
                $.get('./api/user/get-user-info', (data) => {
                    let temp = ''
                    groupNames = []
                    classArr = []
                    for (let i = 0; i < data.group.length; i++) {
                        if (i < 3) {
                            if (data.group[i].picture === '') {
                                temp += '<li class="img' + (i + 1) + '"></li>'
                            }
                            else {
                                temp += '<li class="img' + (i + 1) + '"><img src="' + data.group[i].picture + '"></li>'
                            }
                            classArr.push('img' + (i + 1))
                        }
                        else {
                            if (data.group[i].picture === '') {
                                temp += '<li class="img-none"><img src="' + data.group[i].picture + '"></li>'
                            } else {
                                temp += '<li class="img-none"></li>'
                            }
                            classArr.push('img-none')
                        }
                        let group = {'group_name': data.group[i].group_name, 'group_id': data.group[i].group_id}
                        groupNames.push(group)
                    }
                    // 新增討論區選項
                    if (groupNames.length < 3) {
                        temp += '<li class="img' + (groupNames.length + 1) + '"></li>'
                        classArr.push('img' + (groupNames.length + 1))
                    } else {
                        temp += '<li class="img-none"></li>'
                        classArr.push('img-none')
                    }
                    groupNames.push({'group_name': '討論區', 'group_id': 0})
                    // 處理不足3個
                    if (groupNames.length === 1) {
                        temp += '<li class="img2"></li><li class="img3"></li>'
                        classArr.push('img2')
                        classArr.push('img3')
                        /////////////////////////////////////改道這!!!
                        groupNames.push({'group_name': '討論區', 'group_id': 0})
                        groupNames.push({'group_name': '討論區', 'group_id': 0})
                    } else if (groupNames.length === 2) {
                        temp += '<li class="img3"></li><li class="img-none"></li>'
                        classArr.push('img3')
                        classArr.push('img-none')
                        groupNames.push(groupNames[0])
                        groupNames.push({'group_name': '討論區', 'group_id': 0})
                    }
                    $('.choose-group-page ul.imgbox').html(temp)
                    $('.choose-group-page .choose-group-name').text(groupNames[1].group_name)
                    if($('.choose-group-page .choose-group-name').text() === '討論區') {
                        $('.choose-group-page .choose-group-enter').text('進入討論區')
                    }
                })
                $('.choose-group-page').transition('slide up')
            }
        }).fail(() => {
            $('.login-error-msg').html('系統錯誤請稍後再試！')
        })
    }
})

// 註冊頁面btn
$('.sign-up-page i').click((event) => {
    event.preventDefault()
    $('.sign-up-page').transition('slide up')
    $('.entrance-title').css('transform', 'none')
    $('.sign-up-error-msg').html('')
    $('.sign-up-page input[name=email]').val('')
    $('.sign-up-page input[name=name]').val('')
    $('.sign-up-page input[name=pwd]').val('')
    $('.sign-up-page input[name=pwd-again]').val('')
})

$('.sign-up-button-div button:nth-child(1)').click((event) => {
    event.preventDefault()
    if ($('.sign-up-page input[name=email]').val() === '' || $('.sign-up-page input[name=name]').val() === '' || $('.sign-up-page input[name=pwd]').val() === '' || $('.sign-up-page input[name=pwd-again]').val() === '') {
        $('.sign-up-error-msg').html('請輸入完整資訊')
    }
    else if ($('.sign-up-page input[name=pwd]').val() != $('.sign-up-page input[name=pwd-again]').val()) {
        $('.sign-up-error-msg').html('再次輸入密碼錯誤請重新輸入')
    } else {
        $('.sign-up-error-msg').html('')
        $.get('./api/auth/check-email-exist', {
            email: $('.sign-up-page input[name=email]').val()
        }, (data1) => {
            if (data1) {
                $('.sign-up-error-msg').html('此email已註冊或已產生驗證碼')
            } else {
                $.post('./api/auth/signup', {
                    email: $('.sign-up-page input[name=email]').val(),
                    username: $('.sign-up-page input[name=name]').val(),
                    password: $('.sign-up-page input[name=pwd]').val()
                }, (data2) => {
                    if (data2) {
                        $('.sign-up-page').transition('slide up')
                        $('.verification-page div:nth-child(2) h2').text('寄送驗證碼至以下信箱')
                        $('.verification-page input[name=email]').val($('.sign-up-page input[name=email]').val())
                        $('.verification-page input[name=email]').disabled = true
                        $('.entrance-title').css('transform', 'translateY(-8vh)')
                        $('.verification-page').transition('slide up')
                    }else {
                        $('.sign-up-error-msg').html('系統錯誤，請稍後再嘗試')
                    }
                })
            }
        })
    }
})

$('.sign-up-button-div button:nth-child(2)').click((event) => {
    event.preventDefault()
    $('.sign-up-page').transition('slide up')
    $('.entrance-title').css('transform', 'translateY(-8vh)')
    $('.verification-page').transition('slide up')
})

// 驗證頁面btn
$('.verification-page i').click((event) => {
    event.preventDefault()
    $('.verification-page').transition('slide up')
    $('.verification-page div:nth-child(2) h2').text('請輸入註冊使用的信箱')
    $('.verification-page input[name=email]').val('')
    $('.verification-page input[name=email]').disabled = false
    $('.verification-page input[name=verification-code]').val('')
    $('.verification-error-msg').html('')
    $('.entrance-title').css('transform', 'translateY(-15vh)')
    $('.sign-up-page').transition('slide up')
})

$('.verification-page button').click((event) => {
    event.preventDefault()
    let temp = true
    $('.verification-error-msg').html('')
    if ($('.verification-page input[name=email]').disabled === false) {
        $.get('./api/auth/check-email-exist', {
            email: $('.sign-up-page input[name=email]').val()
        }, (data) => {
            if (!data) {
                temp = false
                $('.verification-error-msg').html('此email尚未註冊')
            }
        })
    }
    if (temp) {
        $.get('./api/auth/check-verification-code', {
            email: $('.verification-page input[name=email]').val(),
            verify_code:$('.verification-page input[name=verification-code]').val()
        }, (data) => {
            if (data) {

                $('.verification-page').transition('slide up')
                let temp = '<li class="img1"></li><li class="img2"></li><li class="img3"></li>'
                groupNames = [{'group_name': '討論區', 'group_id': 0}, {'group_name': '討論區', 'group_id': 0}, {'group_name': '討論區', 'group_id': 0}]
                classArr = ['img1', 'img2', 'img3']
                $('.choose-group-page ul.imgbox').html(temp)
                $('.choose-group-page .choose-group-name').text(groupNames[1].group_name)
                $('.choose-group-page .choose-group-enter').text('進入討論區')
                // $('.choose-group-page').transition('slide up')
            }else {
                $('.verification-error-msg').html('驗證碼錯誤')
            }
        })
    }
})

// 選擇群組頁面btn
$('.choose-group-enter').click(() => {
    if (groupNames[1].group_id === 0) {
        ///////////不確定
        window.location = "./forum.html?page=forum-main-page"
    } else {
        window.location = "./main.html?group-id=" + groupNames[1].group_id
    }
})

$('.choose-group-create').click(() => {
    $('.choose-group-page').transition('slide up')
    $('.create-group-page').transition('slide up')
})

$('.choose-group-join').click(() => {
    $('.choose-group-page').transition('slide up')
    $('.join-group-page').transition('slide up')
})

$('.group-box i.left').click(() => {
    let firstValue = classArr.shift()
    let firstName = groupNames.shift()
    classArr.push(firstValue)
    groupNames.push(firstName)
    let img =  $('.imgbox').children()
    for(let i = 0; i < classArr.length; i++) {
        img[i].className = classArr[i]
    }
    $('.choose-group-page .choose-group-name').text(groupNames[1].group_name)
    if (groupNames[1].group_name === '討論區') {
        $('.choose-group-page .choose-group-enter').text('進入討論區')
    } else {
        $('.choose-group-page .choose-group-enter').text('進入群組')
    }
})

$('.group-box i.right').click(() => {
    let lastValue = classArr.pop()
    let lastName = groupNames.pop()
    classArr.unshift(lastValue)
    groupNames.unshift(lastName)
    let img =  $('.imgbox').children()
    for(let i = 0; i < classArr.length; i++) {
        img[i].className = classArr[i]
    }
    $('.choose-group-page .choose-group-name').text(groupNames[1].group_name)
    if (groupNames[1].group_name === '討論區') {
        $('.choose-group-page .choose-group-enter').text('進入討論區')
    } else {
        $('.choose-group-page .choose-group-enter').text('進入群組')
    }
})

// 創立群組頁面btn
$('.create-group-page .chevron.left.icon').click(() => {
    $('.create-group-page').transition('slide up')
    $('.choose-group-page').transition('slide up')
    $('.create-group-page select[name=group-kind]').val('travel')
    $('.create-group-page select[name=group-currency]').val('TWD')
    $('.create-group-page input[name=group-name]').val('')
    $('.create-group-page input[name=group-balance]').val('')
    $('.create-group-page input[name=group-first-transaction]').val('')
    $('.create-group-page input[name=group-refill]').val('')
    $('.create-group-error-msg').html('')

})

let groupName, groupCurrency, groupKind, groupBalance, groupTransaction, groupRefill
$('.create-group-page button').click((event) => {
    event.preventDefault()
    if ($('.create-group-page input[name=group-name]').val() === '' || $('.create-group-page input[name=group-balance]').val() === '' || $('.create-group-page input[name=group-first-transaction]').val() === '' || $('.create-group-page input[name=group-refill]').val() === '') {
        $('.create-group-error-msg').html('請輸入完整資訊')
    } else {
        $('.create-group-error-msg').html('')
        groupName = $('.create-group-page input[name=group-name]').val()
        groupCurrency = $('.create-group-page select[name=group-currency]').val()
        groupKind = $('.create-group-page select[name=group-kind]').val()
        groupBalance = $('.create-group-page input[name=group-balance]').val()
        groupTransaction = $('.create-group-page input[name=group-first-transaction]').val()
        groupRefill = $('.create-group-page input[name=group-refill]').val()
        $('.create-group-page').transition('slide up')
        $('.who-am-i-page button').text('創立群組')
        $('.who-am-i-page').transition('slide up')
    }
})

// 加入群組頁面btn
$('.join-group-page .chevron.left.icon').click(() => {
    $('.join-group-page').transition('slide up')
    $('.choose-group-page').transition('slide up')
    $('.join-group-page input[name=group-id]').val('')
    $('.join-group-page input[name=group-pwd]').val('')
    $('.join-group-error-msg').html('')
})

let verifyCode, invitationCode
$('.join-group-page button').click((event) => {
    event.preventDefault()
    if ($('.join-group-page input[name=group-id]').val() === '' || $('.join-group-page input[name=group-pwd]').val() === '') {
        $('.join-group-error-msg').html('請輸入群組ID及密碼！')
    } else {
        $('.join-group-error-msg').html('')
        invitationCode = $('.join-group-page input[name=group-id]').val()
        verifyCode = $('.join-group-page input[name=group-pwd]').val()
        $.get('./api/group/check-group-accessible', {
            invite_code: invitationCode,
            verify_code: verifyCode
        }, (data) => {
            if (!data) {
                $('.join-group-error-msg').html('輸入群組ID或密碼錯誤！')
            } else {
                $('.join-group-page').transition('slide up')
                $('.who-am-i-page button').text('加入群組')
                $('.who-am-i-page').transition('slide up')
            }
        }).fail(() => {
            $('.join-group-error-msg').html('系統錯誤請稍後再試！')
        })
    }
})

// 我是誰頁面btn
$('.who-am-i-page .chevron.left.icon').click(() => {
    $('.who-am-i-page').transition('slide up')
    if ($('.who-am-i-page button').text() == '加入群組') {
        $('.join-group-page').transition('slide up')
    } else {
        $('.create-group-page').transition('slide up')
    }
    $('.who-am-i-page input[name=nickname]').val('')
    $('.who-am-i-error-msg').html('')
})

let groupId = 0
$('.who-am-i-page button').click((event) => {
    event.preventDefault()
    if ($('.who-am-i-page input[name=nickname]').val() === '') {
        $('.who-am-i-error-msg').html('請輸入你的暱稱！')
    } else {
        if ($('.who-am-i-page button').text() === '創立群組') {
            $.post('./api/group/creat-group', {
                group_name: groupName,
                nickname: $('.who-am-i-page input[name=nickname]').val(),
                type: groupKind,
                currency: groupCurrency,
                min_balance: groupBalance,
                first_remittance: groupTransaction,
                top_up_each_time: groupRefill,
                picture: ''
            }, (data) => {
                groupId = data.group_id
                $('.who-am-i-error-msg').html('')
                window.location = "./main.html?group-id=" + groupId
            }).fail(() => {
                $('.who-am-i-error-msg').html('系統錯誤請稍後再試！')
            })
        } else {
            $.post('./api/group/join-group', {
                invite_code: invitationCode,
                verify_code: verifyCode,
                nickname: $('.who-am-i-page input[name=nickname]').val()
            }, (data) => {
                groupId = data.group_id
                $('.who-am-i-error-msg').html('')
                window.location = "./main.html?group-id=" + groupId
            }).fail(() => {
                $('.who-am-i-error-msg').html('系統錯誤請稍後再試！')
            })
        }
    }
})
