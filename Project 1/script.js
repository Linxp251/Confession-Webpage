













// 选着no时改变no选项的内容数组
const no_messages=[
    "是吗？",
    "你确定？",
    "......"
];

// 数组索引，用于选择输出哪条提示信息
let messageIndex=0;


// 给YES添加点击事件
document.querySelector('.yes-button').addEventListener('click',()=>{
    window.location.href="./yes-index.html"
})
// 给no添加点击事件
document.querySelector('.no-button').addEventListener('click',()=>{
    // 1.改变no按钮内容

    const nobtn=document.querySelector('.no-button');
    const yesbtn=document.querySelector(".yes-button");
    nobtn.textContent=no_messages[messageIndex];
    messageIndex=(messageIndex+1)%no_messages.length;
    // 2.改变按钮大小(yes增大，no不变)

    // 获取当前yes按钮的大小，并将它放大1.5倍

    const currentSize= parseFloat(window.getComputedStyle(yesbtn).fontSize);

    yesbtn.style.fontSize=`${currentSize*1.5}px`

})
