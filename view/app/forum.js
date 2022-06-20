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
