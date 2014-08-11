$(document).ready(function () {

    var TIME_TO_INITIAL_HIDE = 1000;

    // Initial animation to hide the overlay
    var hideTimer = setTimeout(function() {
        $('#overlay').fadeOut();
    }, TIME_TO_INITIAL_HIDE);

    // Just hide or show our overlay if clicked on any container
    $('#comic, #overlay').on("dblclick", function (e) {
        $('#overlay').fadeToggle();

        // If user forced to hide, then ignore our initial animation
        clearTimeout(hideTimer);
    });
});