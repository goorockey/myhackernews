$(".vote_img").click(function(){
    $(this).hide();
    $.get($(this).attr("href"));
    return false;
})
