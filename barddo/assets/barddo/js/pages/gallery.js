$(document).ready(function () {
    $('.vote').click(function (e) {
        Dajaxice.rating.toggle_rating(Dajax.process, { 'work_id': $(this).attr("data-work-id") });
        $(this).html('<i class="icon-star-empty"></i>');
        $(this).removeClass("liked");

        $(this).addClass("waiting");
        $(this).html('<i class="icon-spinner icon-spin white"></i>');

        e.preventDefault();
        e.stopPropagation();
        return false;
    });

});

function set_rating(work_id, liked) {
    var icon_element = $("a[data-work-id=" + work_id + "]");

    icon_element.removeClass("waiting");
    if (liked) {
        icon_element.addClass("liked");
        icon_element.html('<i class="icon-star"></i>');
    } else {
        icon_element.addClass("liked");
        icon_element.html('<i class="icon-star-empty"></i>');
    }
}
