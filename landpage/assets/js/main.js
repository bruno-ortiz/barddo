$(function () {

    /*==========  Initalize steller for parrallax header  ==========*/

    //$.stellar();

    /*==========  Initalize fit text for responsive text  ==========*/

    setInterval(function () {
        $(".fittext").fitText();
        $(".littext").fitText(0.8, {maxFontSize: '40px'});
        $(".slug").fitText(0.8, {maxFontSize: '50px'});
    }, 500);


    /*==================================================================
     =            Hide elements if browser suppots animation            =
     ==================================================================*/


    if (!Modernizr.cssanimations) {
        //dont hide everything
    } else {
        $('.story-container, .story-image-container, .dot-container, .hr-container, .footer-container ').children().addClass('hide');
    }

    /*-----  End of Hide elements if browser suppots animation  ------*/


    /*=========================================================
     =            Use waypoint to trigger animation            =
     =========================================================*/


    $('.story-container, .story-image-container, .dot-container, .hr-container, .footer-container ').waypoint(function (direction) {

        if (direction == 'down') {

            if ($(this).children().data('delay') !== undefined) {
                var delay = $(this).children().data('delay');
            } else {
                var delay = 0;
            }

            $(this).children().removeClass("hide").addClass("animated fadeInDown delay-" + delay);

        } else {

            $(this).children().addClass("hide").removeClass("animated fadeInDown");

        }

    }, { offset: '55%' });


    /*-----  End of Use waypoint to trigger animation  ------*/

    /*======================================================
     =            Waypoint for background colour            =
     ======================================================*/

    $('.color-change').waypoint(function (direction) {

        var colorUp = {
            backgroundColor: $(this).data('colorup')
        };
        var colorDown = {
            backgroundColor: $(this).data('colordown')
        };

        if (direction == 'down') {

            $('body').animate(colorDown, 525);

        } else {

            $('body').animate(colorUp, 525);

        }

    }, { offset: '70%' });


    /*-----  End of Waypoint for background colour  ------*/


    /*===========================================
     =            Waypoint for header            =
     ===========================================*/

    $('#start').waypoint(function (direction) {

        if (direction == 'down') {

            $('#story-icons, #sub-title').fadeTo("300ms", 0);

        } else {

            $('#story-icons, #sub-title').fadeTo("300ms", 1);

        }

    }, { offset: '55%' });


    /*-----  End of Waypoint for header  ------*/


});