/**
 * Called when the collection name provided is no avaliable.
 * Should handle error class and messages to the user.
 */
function callback_collection_name_is_not_avaliable() {
    $("#collection-name-group").removeClass("has-success has-info").addClass("has-error")
    $("#collection-name-group i").removeClass().addClass("icon-exclamation-sign")
    $("#collection-next").prop('disabled', true);

    error_tooltip('#collection-name-validation', 'Name already in use!')
}

/**
 * Called when the collection name provided is avaliable.
 * Should handle success class and messages to the user.
 */
function callback_collection_name_is_avaliable() {
    $("#collection-name-group").removeClass("has-error has-info").addClass("has-success")
    $("#collection-name-group i").removeClass().addClass("icon-ok-sign")
    $("#collection-next").prop('disabled', false);

    $("#id_name").val($('#collection-name-validation').val())
}

/**
 * Method that check on the server if the collection provided is unique and give
 * the feedback to the user
 */
function callback_collection_name_event() {
    $('#collection-name-validation').on("keyup", function () {
        delay(function () {
            var name = $('#collection-name-validation').val();
            if (name.length > 2) {
                Dajaxice.core.validate_unique_collection(Dajax.process, {
                    'collection_name': $('#collection-name-validation').val()
                });

                $('#collection-name-group i').removeClass('icon-info-sign').addClass('icon-spinner icon-spin');
            }
        }, 1000);
    });
}