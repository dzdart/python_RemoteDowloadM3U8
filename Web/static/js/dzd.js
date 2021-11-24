function randomString(len) {
　　len = len || 32;
　　var $chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';    /****默认去掉了容易混淆的字符oOLl,9gq,Vv,Uu,I1****/
　　var maxPos = $chars.length;
　　var pwd = '';
　　for (i = 0; i < len; i++) {
　　　　pwd += $chars.charAt(Math.floor(Math.random() * maxPos));
　　}
　　return pwd;
}



function send_post(){
    var m3_url=document.getElementsByName('m3u8_url')[0].value
    var save_name=document.getElementsByName('save_name')[0].value
    var save_dir=document.getElementsByName('save_dir')[0].value
    var httpRequest = new XMLHttpRequest(); //创建请求对象

    httpRequest.open('POST', 'http://127.0.0.1:8090/test', true); //打开请求
    httpRequest.setRequestHeader("Content-type","application/x-www-form-urlencoded");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
    httpRequest.send('url='+m3_url+'&'+'save_name='+save_name+'&'+'save_dir='+save_dir);//发送请求 将情头体写在send中

    httpRequest.onreadystatechange = function(){
    //请求成功后的任务
    if (httpRequest.readyState == 4 && httpRequest.status == 200) {//如果返回的状态吗为200则执行
        var json = JSON.parse(httpRequest.responseText)['id'];
        document.getElementsByName('m3u8_id')[0].style="block";
        document.getElementsByName('m3u8_id')[0].value=json;
        document.getElementById('loading_pic').style.display="none";
        console.log(json);
        }
    }

}

function refresh(){
    console.log("这是一个刷新事件");
}

function check_info(){
    var m3_url=document.getElementsByName('m3u8_url')[0].value
    var save_name=document.getElementsByName('save_name')[0].value
    var save_dir=document.getElementsByName('save_dir')[0].value
    if (m3_url != ''|save_name !=''|save_dir !=''){
    return 1
    }else{return 0}
}

function show_tips(){
    var tips = document.getElementById('message_box');
    var input = document.getElementById('video_id')
    console.log(tips.style.display)
    if (check_info()){//如果关键信息检查通过才显示
        if (tips.style.display == "none"){
        //如果是隐藏，那么显示
        send_post()
        tips.style.display = "block";

    } else {

        tips.style.display = "none";
    }

    }else{alert("信息不完整")}//否则就显示提示信息

}

function show_player(id){
    //获取要显示的div对象
    var  video_player=document.getElementById('video_player');
    var video_player_player=document.getElementById('video_player_player');
    if (video_player.style.display == "none"){
    //如果为隐藏，则显示并播放
    video_player.style.display="block";
    video_player_player.src="/dd?id="+id;
    video_player_player.play();
    }
    else{
    video_player.style.display="none";
    video_player_player.pause();
    video_player_player.src="";
    }
}
