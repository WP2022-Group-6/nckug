$(document).ready(() => {
    var url = 'http://127.0.0.1'
    var port = '5000'
    var socket = io.connect(url + ':' + port)
    socket.on('update', function () {
        top_update()
    })
})

const urlParams = new URLSearchParams(window.location.search)
let pageNow = urlParams.get('page')
let groupId = urlParams.get('group-id')
if(pageNow === "group-chosing-page") {
    $('.group-chosing-page').transition('toggle')
} else if (pageNow === "group-setting-page") {
    group_setting_refresh()
    $('.group-setting-page').transition('toggle')
} else if (pageNow === "schedule-group-page") {
    schedule_refresh()
    $('.schedule-group-page').transition('toggle')
} else if (pageNow === "forum-main-page") {
    forum_refresh()
    $('.forum-main-page').transition('toggle')
} else if (pageNow === "personal-setting-page") {
    $('.personal-setting-page').transition('toggle')
}

// 彈出側欄選單
$('.side-menu-block').click(() => {
    $('.side-menu-page').transition('slide right')
})

$('.group-setting-bar i').click(() => {
    if ($('.group-setting-bar i').hasClass('chevron')) {
        if(!$('.group-basic-setting').hasClass('hidden')) {
            $('.group-basic-setting').transition('toggle')
        } else if (!$('.group-notice-setting').hasClass('hidden')) {
            $('.group-notice-setting').transition('toggle')
        }else if (!$('.group-add-setting').hasClass('hidden')) {
            $('.group-add-setting').transition('toggle')
        }
        $('.group-setting-bar i').toggleClass('align justify chevron left')
        $('.group-setting-choose').transition('toggle')
    } else {
        $('.side-menu-page').transition('slide right')
    }

})
$('.group-chosing-bar i.align.justify').click(() => {
    $('.side-menu-page').transition('slide right')
})
$('.schedule-group-bar i.align.justify').click(() => {
    $('.side-menu-page').transition('slide right')
})
$('.forum-main-bar i.align.justify').click(() => {
    $('.side-menu-page').transition('slide right')
})
$('.title-with-icon i.align.justify').click(() => {
    $('.side-menu-page').transition('slide right')
})

$('.side-menu-choose-group h3').click(() => {
    if (pageNow != "group-chosing-page") {
        $('.' + pageNow).transition('toggle')
        pageNow = 'group-chosing-page'
        $('.' + pageNow).transition('toggle')
    }
    $('.side-menu-page').transition('slide right')
})

$('.side-menu-group-setting h3').click(() => {
    if (pageNow != "group-setting-page") {
        $('.' + pageNow).transition('toggle')
        pageNow = 'group-setting-page'
        $('.' + pageNow).transition('toggle')
    }
    group_setting_refresh()
    $('.side-menu-page').transition('slide right')
})

$('.side-menu-schedule h3:nth-child(2)').click(() => {
    if (pageNow != "schedule-group-page") {
        $('.' + pageNow).transition('toggle')
        pageNow = 'schedule-group-page'
        $('.' + pageNow).transition('toggle')
    }
    schedule_refresh()
    $('.side-menu-page').transition('slide right')
})

$('.side-menu-schedule h3:nth-child(3)').click(() => {
    if (pageNow != "forum-main-page") {
        $('.' + pageNow).transition('toggle')
        pageNow = 'forum-main-page'
        $('.' + pageNow).transition('toggle')
    }
    forum_refresh()
    $('.side-menu-page').transition('slide right')
})

$('.side-menu-personal-setting h3:nth-child(3)').click(() => {
    if (pageNow != "personal-setting-page") {
        $('.' + pageNow).transition('toggle')
        pageNow = 'personal-setting-page'
        $('.' + pageNow).transition('toggle')
    }
    $('.side-menu-page').transition('slide right')
})

// 選擇群組
classArr = ['img1', 'img2', 'img3', 'img-none', 'img-none']
$('.group-box i.left').click(() => {
    let firstValue = classArr.shift()
    classArr.push(firstValue)
    let img =  $('.imgbox').children()
    for(let i = 0; i < classArr.length; i++) {
        img[i].className = classArr[i]
    }
})

$('.group-box i.right').click(() => {
    let lastValue = classArr.pop()
    classArr.unshift(lastValue)
    let img =  $('.imgbox').children()
    for(let i = 0; i < classArr.length; i++) {
        img[i].className = classArr[i]
    }
})

// 群組設定
$('.group-setting-choose button:nth-child(1)').click(() => {
    $('.group-setting-choose').transition('toggle')
    $('.group-basic-setting').transition('toggle')
    $('.group-setting-bar i').toggleClass('align justify chevron left')
})

$('.group-setting-choose button:nth-child(2)').click(() => {
    $('.group-setting-choose').transition('toggle')
    $('.group-notice-setting').transition('toggle')
    $('.group-setting-bar i').toggleClass('align justify chevron left')
})

$('.group-setting-choose button:nth-child(3)').click(() => {
    $('.group-setting-choose').transition('toggle')
    $('.group-add-setting').transition('toggle')
    $('.group-setting-bar i').toggleClass('align justify chevron left')
})

$('.group-basic-setting button').click(() => {
    $.post('/api/group/set-group-info', {
        group_id: groupId,
        currency: $('.group-basic-setting select[name=group-currency]').val(),
        type: $('.group-basic-setting select[name=group-kind]').val()
    }, () => {
        $('.group-basic-setting').transition('toggle')
        $('.group-setting-choose').transition('toggle')
        $('.group-setting-bar i').toggleClass('align justify chevron left')
    })
})

$('.group-notice-setting button').click(() => {
    $.post('/api/group/set-group-info', {
        group_id: groupId,
        min_balance: $('.group-notice-setting input[name=group-balance]').val(),
        top_up_each_time: $('.group-notice-setting input[name=group-refill]').val()
    }, () => {
        $('.group-notice-setting').transition('toggle')
        $('.group-setting-choose').transition('toggle')
        $('.group-setting-bar i').toggleClass('align justify chevron left')
    })
})

// 新增行程
$('.schedule-add button').click(() => {
    $.post('/api/journey/set-journey', {
        group_id: groupId,
        date: $('.schedule-add input[name=schedule-data]').val(),
        time: $('.schedule-add input[name=schedule-time]').val(),
        place: $('.schedule-add input[name=schedule-place]').val(),
        note: $('.schedule-add input[name=schedule-note]').val()
    }, (data) => {
        if (data) {
            schedule_refresh()
            $('.schedule-add').transition('slide up')
            $('.schedule-group-bar i:nth-child(2)').toggleClass('edit outline check')
        }
    })
})

$('.schedule-group-bar i:nth-child(2)').click(() => {
    $('.schedule-group-bar i:nth-child(2)').toggleClass('edit outline check')
    $('.schedule-group-item i.ellipsis').toggleClass('hidden')
    $('.schedule-group-content .plus.icon').toggleClass('hidden')
    if (!$('.schedule-group-btn').hasClass('hidden')) {
        $('.schedule-group-btn').toggleClass('hidden')
    }
})

$('.schedule-add-title i.chevron').click(() => {
    $('.schedule-add').transition('slide up')
})

// 新增貼文
$('.forum-main-fixed-i i.edit').click(() => {
    $.get('/api/user/get-user-info', (data) => {
        $('.edit-post-id p').text(data.name)
    })
    $('.forum-main-page').transition('toggle')
    $('.edit-post-page').transition('toggle')
})

$('.edit-post-bar i.arrow.right').click(() => {
    if ($('.edit-post-main input[name=post-title]').val() === '' || $('.edit-post-main textarea[name=post-content]').val() === '') {
        /// error handler
    } else {
        console.log($('.edit-post-main input[name=post-title]').val())
        console.log($('.edit-post-main textarea[name=post-content]').val())
        $.post('/api/post/new-post', {
            title: $('.edit-post-main input[name=post-title]').val(),
            content: $('.edit-post-main textarea[name=post-content]').val()
        }, (data) => {
            if(data) {
                $('.edit-post-page').transition('toggle')
                forum_refresh()
                $('.forum-main-page').transition('toggle')
            }
        })
    }
})

$('.read-post-bar i.chevron.left').click(() => {
    $('.read-post-page').transition('toggle')
    forum_refresh()
    $('.forum-main-page').transition('toggle')
})

$('.read-post-like i.heart').click(() => {
    let temp
    console.log(postId)
    if ($('.read-post-like i.heart').hasClass('outline')) {
        temp = 'True'
    } else {
        temp = 'False'
    }
    $.post('/api/post/new-response', {
        post_id: postId,
        like: temp
    }, (data) => {
        if (data) {
            $('.read-post-like i.heart').toggleClass('outline')
            $('.read-post-response i.heart').toggleClass('outline')
        }
    })
})

$('.read-post-like i.bookmark').click(() => {
    let temp
    if ($('.read-post-like i.bookmark').hasClass('outline')) {
        temp = 'True'
    } else {
        temp = 'False'
    }
    $.post('/api/post/new-response', {
        post_id: postId,
        collection: temp
    }, (data) => {
        if (data) {
            $('.read-post-like i.bookmark').toggleClass('outline')
            $('.read-post-response i.bookmark').toggleClass('outline')
        }
    })
})

$('.read-post-response button').click(() => {
    if ($('.read-post-response input').val() != '') {
        $.post('/api/post/new-comment', {
            post_id: postId,
            content: $('.read-post-response input').val()
        }, (data) => {
            if (data) {
                let tempName
                let temp
                $.get('/api/user/get-user-info', (data) => {
                    tempName = data.name
                    temp = '<div class="read-post-comment"><div class="read-post-comment-id"><div></div><p>' + tempName +'</p></div><div><p>' + $('.read-post-response input').val() + '</p></div></div>'
                    $('.read-post-comments').append(temp)
                    $('.read-post-response input').val('')
                })
            }
        })
    }
})

// refresh function
function group_setting_refresh() {
    $.get('/api/group/get-group-info', {
        group_id: groupId
    }, (data) => {
        $('.group-setting-pic p').text(data.group_name)
        $('.group-basic-setting select[name=group-currency]').val(data.currency)
        $('.group-basic-setting select[name=group-kind]').val(data.type)
        $('.group-notice-setting input[name=group-balance]').val(data.min_balance)
        $('.group-notice-setting input[name=group-refill]').val(data.top_up_each_time)
        $('.group-add-setting').html('')
        for (let i = 0; i < data.member.length; i++) {
            let tempDiv = document.createElement('div')
            let tempPic = document.createElement('div')
            let tempName = document.createElement('h3')
            tempName.textContent = data.member[i].nickname
            tempDiv.appendChild(tempPic)
            tempDiv.appendChild(tempName)
            $('.group-add-setting').append(tempDiv)
        }
        let tempDiv = document.createElement('div')
        tempDiv.classList.add('group-invite')
        let tempPic = document.createElement('div')
        let tempName = document.createElement('h3')
        tempName.textContent = '邀請其他朋友'
        tempDiv.appendChild(tempPic)
        tempDiv.appendChild(tempName)
        $('.group-record').append(tempDiv)
        document.querySelector('.group-invite').addEventListener('click', function () {
            $('.send-invitation-page .invitation-group-name').text(data.group_name)
            $('.send-invitation-page div:nth-child(2) h3:nth-child(2)').text(data.invite_code)
            $('.send-invitation-page div:nth-child(2) h3:nth-child(4)').text(data.verify_code)
            // 複製邀請資訊尚未實作
            $('.send-invitation-page').transition('slide up')
        })
    })
}

function schedule_refresh() {
    $.get('/api/group/get-group-info', {
        group_id: groupId
    }, (data) => {
        $('.schedule-group-pic h3').text(data.group_name)
        $.get('/api/journey/get-journey', {
            group_id: groupId
        }, (data) => {
            $('.schedule-group-content').html('')
            for (let i = 0; i < data.length; i++) {
                let tempH3 = document.createElement('h3')
                tempH3.classList.add('schedule-group-day')
                tempH3.textContent = data[i].date.slice(5) + ' Day' + data[i].day
                $('.schedule-group-content').append(tempH3)
                for (let j = 0; j < data[i].journey.length; j++) {
                    let tempDiv = document.createElement('div')
                    tempDiv.classList.add('schedule-group-item')
                    let tempDiv1 = document.createElement('div')
                    tempDiv1.classList.add('schedule-group-btn', 'transition', 'hidden')
                    let tempI1 = document.createElement('i')
                    tempI1.classList.add('trash', 'alternate', 'icon')
                    let tempI2 = document.createElement('i')
                    tempI2.classList.add('edit', 'outline', 'icon')
                    tempDiv1.appendChild(tempI1)
                    tempDiv1.appendChild(tempI2)
                    let tempI3 = document.createElement('i')
                    tempI3.classList.add('ellipsis', 'horizontal', 'icon', 'transition', 'hidden')
                    let tempDiv2 = document.createElement('div')
                    let tempH31 = document.createElement('h3')
                    tempH31.textContent = data[i].journey[j].time
                    let tempH32 = document.createElement('h3')
                    tempH32.textContent = data[i].journey[j].place
                    tempDiv2.appendChild(tempH31)
                    tempDiv2.appendChild(tempH32)
                    let tempH33 = document.createElement('h3')
                    tempH33.classList.add('schedule-group-note')
                    tempH33.textContent = data[i].journey[j].note
                    tempDiv.appendChild(tempDiv1)
                    tempDiv.appendChild(tempI3)
                    tempDiv.appendChild(tempDiv2)
                    tempDiv.appendChild(tempH33)
                    console.log(i+j)
                    console.log(document.querySelectorAll('.schedule-group-item i.ellipsis'))
                    console.log(document.querySelectorAll('.schedule-group-btn'))
                    $('.schedule-group-content').append(tempDiv)
                    document.querySelectorAll('.schedule-group-item i.ellipsis')[i + j].addEventListener('click', () => {
                        if (document.querySelectorAll('.schedule-group-btn')[i + j].classList.contains('hidden')) {
                            document.querySelectorAll('.schedule-group-btn')[i + j].classList.remove('hidden')
                        } else {
                            document.querySelectorAll('.schedule-group-btn')[i + j].classList.add('hidden')
                        }
                    })
                    document.querySelectorAll('.schedule-group-btn i.trash')[i + j].addEventListener('click', () => {
                        console.log(data[i].journey[j].journey_id)
                        $.post('/api/journey/set-journey', {
                            journey_id: data[i].journey[j].journey_id,
                            delete: 'True'
                        }, (data) => {
                            if (data) {
                                schedule_refresh()
                                $('.schedule-group-bar i:nth-child(2)').toggleClass('edit outline check')
                            }
                        })
                    })
                }
            }
            let tempI = document.createElement('i')
            tempI.classList.add('big', 'plus', 'icon', 'transition', 'hidden')
            $('.schedule-group-content').append(tempI)
            document.querySelector('.schedule-group-content .plus.icon').addEventListener('click', () => {
                $('.schedule-add').transition('slide up')
            })
        })
    })
}

let postId
function forum_refresh() {
    $.get('/api/post/get-post', {
        amount: 20
    }, (data) => {
        $('.forum-main-posts').html('')
        for (let i =0; i < data.length; i++) {
            let tempDiv = document.createElement('div')
            tempDiv.classList.add('forum-main-post')
            let tempP1 = document.createElement('p')
            tempP1.textContent = data[i].owner
            let tempH3 = document.createElement('h3')
            tempH3.textContent = data[i].title
            let tempP2 = document.createElement('p')
            tempP2.textContent = data[i].content.slice(0, 30) + '...'
            tempDiv.appendChild(tempP1)
            tempDiv.appendChild(tempH3)
            tempDiv.appendChild(tempP2)
            let tempDivD = document.createElement('div')
            let tempDiv1 = document.createElement('div')
            let tempI1 = document.createElement('i')
            tempI1.classList.add('heart', 'icon')
            let tempP3 = document.createElement('p')
            tempP3.textContent = data[i].like_amount
            tempDiv1.appendChild(tempI1)
            tempDiv1.appendChild(tempP3)
            let tempDiv2 = document.createElement('div')
            let tempI2 = document.createElement('i')
            tempI2.classList.add('bookmark', 'icon')
            let tempP4 = document.createElement('p')
            tempP4.textContent = data[i].collection_amount
            tempDiv2.appendChild(tempI2)
            tempDiv2.appendChild(tempP4)
            let tempDiv3 = document.createElement('div')
            let tempI3 = document.createElement('i')
            tempI3.classList.add('comment', 'icon')
            let tempP5 = document.createElement('p')
            tempP5.textContent = data[i].comment_amount
            tempDiv3.appendChild(tempI3)
            tempDiv3.appendChild(tempP5)
            tempDivD.appendChild(tempDiv1)
            tempDivD.appendChild(tempDiv2)
            tempDivD.appendChild(tempDiv3)
            tempDiv.appendChild(tempDivD)
            $('.forum-main-posts').append(tempDiv)
            console.log(document.querySelectorAll('.forum-main-post'))
            document.querySelectorAll('.forum-main-post')[i].addEventListener('click', () => {
                $('.read-post-bar h2').text(data[i].title)
                $('.read-post-id p').text(data[i].owner)
                $('.read-post-main h1').text(data[i].title)
                $('.read-post-main textarea').val(data[i].content)
                $('.read-post-main textarea').css('height', calcHeight($('.read-post-main textarea').val() + "px"))
                postId = data[i].post_id
                $('.read-post-message-bar div:nth-child(1) p').text(data[i].like_amount)
                $('.read-post-message-bar div:nth-child(2) p').text(data[i].collection_amount)
                $('.read-post-message-bar div:nth-child(3) p').text(data[i].comment_amount)
                if(data[i].like && $('.read-post-like i.heart').hasClass('outline')) {
                    $('.read-post-like i.heart').toggleClass('outline')
                    $('.read-post-response i.heart').toggleClass('outline')
                }
                if(data[i].collect && $('.read-post-like i.bookmark').hasClass('outline')) {
                    $('.read-post-like i.bookmark').toggleClass('outline')
                    $('.read-post-response i.bookmark').toggleClass('outline')
                }
                let tempDiv = ''
                for (let j = 0; j < data[i].comment.length; j++) {
                    tempDiv += '<div class="read-post-comment"><div class="read-post-comment-id"><div></div><p>' + data[i].comment[j].user_name +'</p></div><div><p>' + data[i].comment[j].content + '</p></div></div>'
                }
                $('.read-post-comments').html(tempDiv)
                $('.forum-main-page').transition('toggle')
                $('.read-post-page').transition('toggle')
            })
        }
    })
}

function top_update() {
    group_setting_refresh()
    schedule_refresh()
    forum_refresh()
}

function calcHeight(value) {
    let numberOfLineBreaks = (value.match(/\n/g) || []).length
    // min-height + lines x line-height + padding + border
    let newHeight = 25 + numberOfLineBreaks * 25 + 20
    return newHeight
}
