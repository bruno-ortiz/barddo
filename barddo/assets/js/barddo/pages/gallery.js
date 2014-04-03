$(document).ready(function () {
    $('.vote').click(function (e) {

        Dajaxice.rating.toggle_rating(Dajaxice.process, { 'html_id': $(this).id });
        $(this).html('<i class="icon-heart-empty captionicons"></i>');
        $(this).removeClass("liked");

        $(this).addClass("waiting");
        $(this).html('<i class="icon-heart-?? captionicons"></i>');

        e.preventDefault();
        e.stopPropagation();
        return false;
    });

    function set_rating(html_id, liked) {
        $(html_id).removeClass("waiting");
        if (liked) {
            $(html_id).addClass("liked");
            $(html_id).html('<i class="icon-heart captionicons"></i>');
        } else {
            $(html_id).html('<i class="icon-heart-empty captionicons"></i>');
        }
    }

});