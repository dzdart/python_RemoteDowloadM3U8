function showCard() {
 var message = document.getElementById("CCN").value;
 var element = document.getElementById("mycreditcardnumber");
 element.textContent = message;
//for Firefox
 element.innerHTML = message;
 return true;
}
function send(){
    var httpRequest = new XMLHttpRequest();
    httpRequest.open('GET', 'http://127.0.0.1:233/?dzd=5666a', false);//第二步：打开连接  将请求参数写在url中  ps:"./Ptest.php?name=test&nameone=testone"
    httpRequest.send();//第三步：发送请求  将请求参数写在URL中
    console.log(httpRequest.status);
    console.log(httpRequest.responseText);
    var message = document.getElementById("CCN").value;
    var element = document.getElementById("mycreditcardnumber");
    element.textContent = httpRequest.responseText;
     element.innerHTML = httpRequest.responseText;


}

function show_player(){
    //获取要显示的div对象
    var  video_player=document.getElementById('video_player');
    if (video_player.style.display == "none"){
    //如果为隐藏，则显示并播放
    video_player.style.display="block";
    video_player.src="https://blz-videos.nosdn.127.net/1/OverWatch/AnimatedShots/Overwatch_AnimatedShot_CinematicTrailer.mp4";
    video_player.play();
    }
    else{
    video_player.style.display="none";
    video_player.pause();
    }
}
function show_tips(){
    showToast('显示文本内容显显示文本内容显','90%','50px');
}