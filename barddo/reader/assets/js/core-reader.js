function setupSizes() {
    $("#comic-container").width($(window).width()).height($(window).height());
    $("#comic-toolbar").width($('#comic').width());
    $("#comic-wrapper").height($("#comic-container").height() - $('#comic-toolbar').height());
}

function setupSizesAndRedraw() {
    setupSizes();
    $.wowBook("#comic").responsive();
}

function setup_reader_for(thumbs_url) {
    var bookWidth = 640;
    var bookHeight = 999;

    var ratio = bookWidth / bookHeight;

    var displayHeight = $(window).height();
    var displayWidth = displayHeight * ratio;

    console.log("Coords " + displayWidth.toString() + "," + displayHeight.toString());

    $("#comic-wrapper").height($("#comic-container").height() - $('#comic-toolbar').height());

    $('#comic').wowBook({
        width: displayWidth * 2,
        height: displayHeight,
        gutterShadow: true,
        handleWidth: displayWidth,
        updateBrowserURL: false,
        centeredWhenClosed: true,
        curl: false,
        mouseWheel: "zoom",
        bookShadow: false,
        scaleToFit: "#comic-wrapper",

        thumbnails: true,
        thumbnailsSprite: thumbs_url,
        thumbnailWidth: 136,
        thumbnailHeight: 136,
        thumbnailsPosition: 'bottom',
        thumbnailsParent: "#comic-container",
        zoomStep: 0.5,
        pageNumbers: false, zoomBoundingBox: "#comic-wrapper",
        turnPageDuration: 250,
        controls: {
            zoomIn: '#zoomin',
            zoomOut: '#zoomout',
            next: '#next',
            back: '#back',
            first: '#first',
            last: '#last',
            slideShow: '#slideshow',
            flipSound: '#flipsound',
            thumbnails: '#thumbs',
            fullscreen: '#fullscreen'
        },  onFullscreenError: function () {
            var msg = "Fullscreen failed.";
            if (self != top) msg = "This website is blocking full screen mode."
            alert(msg);
        }, flipSoundPath: "http://localhost:8000/static/wow_book/sound/", flipSound: false
    }).css({'display': 'none', 'margin': 'auto'}).fadeIn(1000);

    $(window).resize(setupSizesAndRedraw);
    $("#fullscreen").on("click", setupSizesAndRedraw);
    setupSizesAndRedraw()


    $("#comic-wrapper, #comic-toolbar").on("click", function() {
       if($('.wowbook-thumbnails').is(":visible")) {
            $('.wowbook-thumbnails').fadeOut();
       };
    });

}
