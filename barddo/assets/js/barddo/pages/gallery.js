$(document).ready(function () {
    $('.vote').click(function (e) {
        if ($(this).hasClass("liked")) {
            $(this).html('<i class="icon-heart-empty captionicons"></i>');
            $(this).removeClass("liked");
        } else {
            $(this).html('<i class="icon-heart captionicons"></i>');
            $(this).addClass("liked");
        }

        e.preventDefault();
        e.stopPropagation();
        return false;
    });

    function set_rating(work, liked){
        var icon_element = $("#{}").closest("i.captionicons"); //XXX: Isso está certo?

        if (liked){
            icon_element.html('<i class="icon-heart captionicons"></i>');
        } else {
            icon_element.html('<i class="icon-heart-empty captionicons"></i>');
        }
    }

    function notify_not_logged(){
        //TODO
    }

});