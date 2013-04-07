$(".vote_img").click(function(){
    $(this).hide();

    var ping = new Image();
    ping.src = $(this).attr("href");
    return false;
})
