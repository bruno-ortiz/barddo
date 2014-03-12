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
});