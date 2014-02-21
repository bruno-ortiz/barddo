
$(document).ready(function() {
    $(".collection-view").on("click", function() {
        var id = $(this).attr("data-collection");
        var modalId = "#modal-collection-" + id;
        $(modalId).remove();

        $.ajax({
            url: "modal/collection/" + id,
            success: function(data) {
                $("body").append(data);
                $(modalId).modal("show");
            },
            dataType: 'html'
        });

    });
});