let userId = 0
let groupId = 0

$('.entrance-btn').click((event) => {
    event.preventDefault()
    $('.login-page').transition('slide up')
})

$('.login-btn').click((event) =>{
    event.preventDefault()
    if ($('.login-page input[name=email]').val() === '' || $('.login-page input[name=pwd]').val() === ''){
        $('.login-error-msg').html('Please Enter Your Email And Password.')
    }else {
        $('.login-error-msg').html('')
        $.get('./api/auth/login', {
            email: $('.login-page input[name=email]').val(),
            password: $('.login-page input[name=pwd]').val()
        }, (data) => {
            if (data.user_id === null) {
                $('.login-error-msg').html('Error Email or Password.')
            }
            else {
                userId = data.user_id
                $('.login-page').transition('slide up')
                $.get('./api/get-all-group', {
                    user_id: userId
                }, (data) => {
                    ////// 加上將group渲染至前端的部分
                })
                $('.choose-group-page').transition('slide up')
            }
        }).fail(() =>{
            $('.login-error-msg').html('系統錯誤請稍後再試！')
        })
    }
})

$('.choose-group-create').click(() =>{
    $('.choose-group-page').transition('slide up')
    $('.create-group-page').transition('slide up')
})

$('.create-group-page .arrow.left.icon').click(() =>{
    $('.create-group-page').transition('slide up')
    $('.choose-group-page').transition('slide up')
})

$('.choose-group-join').click(() =>{
    $('.choose-group-page').transition('slide up')
    $('.join-group-page').transition('slide up')
})

$('.join-group-page .arrow.left.icon').click(() =>{
    $('.join-group-page').transition('slide up')
    $('.choose-group-page').transition('slide up')
})

let groupName, groupCurrency, groupKind, groupBalance
$('.create-group-page button').click((event) =>{
    event.preventDefault()
    if ($('.create-group-page input[name=group-name]').val() === '' || $('.create-group-page input[name=group-balance]').val() === '') {
        $('.create-group-error-msg').html('請輸入你的名稱及餘額通知金額！')
    }else {
        $('.create-group-error-msg').html('')
        groupName = $('.create-group-page input[name=group-name]').val()
        groupCurrency = $('.create-group-page select[name=group-currency]').val()
        groupKind = $('.create-group-page select[name=group-kind]').val()
        groupBalance = $('.create-group-page input[name=group-balance]').val()
        $('.create-group-page').transition('slide up')
        $('.who-am-i-page button').text('創立群組')
        $('.who-am-i-page').transition('slide up')
    }
})

let verifyCode = ''
$('.join-group-page button').click((event) =>{
    event.preventDefault()
    if ($('.join-group-page input[name=group-id]').val() === '' || $('.join-group-page input[name=group-pwd]').val() === '') {
        $('.join-group-error-msg').html('請輸入群組ID及密碼！')
    }else {
        $('.join-group-error-msg').html('')
        groupId = $('.join-group-page input[name=group-id]').val()
        verifyCode = $('.join-group-page input[name=group-pwd]').val()
        $.get('./api/check-group-accessible', {
            group_id: groupId,
            verify_code: verifyCode
        }, (data) => {
            if (!data) {
                $('.join-group-error-msg').html('輸入群組ID或密碼錯誤！')
            }else {
                $('.join-group-page').transition('slide up')
                $('.who-am-i-page button').text('加入群組')
                $('.who-am-i-page').transition('slide up')
            }
        }).fail(() =>{
            $('.join-group-error-msg').html('系統錯誤請稍後再試！')
        })
    }
})

$('.who-am-i-page .arrow.left.icon').click(() =>{
    $('.who-am-i-page').transition('slide up')
    if ($('.who-am-i-page button').text() == '加入群組'){
        $('.join-group-page').transition('slide up')
    }else{
        $('.create-group-page').transition('slide up')
    }
})

$('.who-am-i-page button').click((event) =>{
    event.preventDefault()
    if ($('.who-am-i-page input[name=nickname]').val() === '') {
        $('.who-am-i-error-msg').html('請輸入你的暱稱！')
    } else {
        if ($('.who-am-i-page button').text() == '創立群組'){
            $.get('./api/creat-group', {
                group_name: groupName,
                user_id: userId,
                nickname: $('.who-am-i-page input[name=nickname]').val(),
                type: groupKind,
                currency: groupCurrency,
                balance: groupBalance,
                picture: ''
            }, (data) => {
                groupId  = data.group_id
                $('.who-am-i-error-msg').html('')
                window.location = "./main.html?user-id=" + userId + "&group-id=" +groupId
            }).fail(() =>{
                $('.who-am-i-error-msg').html('系統錯誤請稍後再試！')
            })
        }else {
            $.get('./api/join-group', {
                user_id: userId,
                group_id: groupId,
                verify_code: verifyCode,
                nickname: $('.who-am-i-page input[name=nickname]').val()
            }, (data) => {
                $('.who-am-i-error-msg').html('')
                window.location = "./main.html?user-id=" + userId + "&group-id=" +groupId
            }).fail(() =>{
                $('.who-am-i-error-msg').html('系統錯誤請稍後再試！')
            })
        }
    }
})
