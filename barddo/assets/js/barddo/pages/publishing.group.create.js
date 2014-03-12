/**
 * Called when the collection name provided is no avaliable.
 * Should handle error class and messages to the user.
 */
function callback_group_name_is_not_avaliable() {
    var $group = $("#group-name-validation");
    $group.removeClass("has-success has-info").addClass("has-error");
    $group.find("i").removeClass().addClass("icon-exclamation-sign");
    $("#collection-next").prop('disabled', true);

    error_tooltip('#collection-name-validation', 'Name already in use!', 3000, 'top')
}

/**
 * Called when the collection name provided is avaliable.
 * Should handle success class and messages to the user.
 */
function callback_group_name_is_avaliable() {
    var $group = $("#group-name-validation");
    $group.removeClass("has-error has-info").addClass("has-success");
    $group.find("i").removeClass().addClass("icon-ok-sign");
    $("#collection-next").prop('disabled', false);

    $("#id_name").val($('#collection-name-validation').val())
}

/**
 * Method that check on the server if the a publishing group name provided is unique and give
 * the feedback to the user
 */
$('#groupNameInput').on('keyup', function () {
    delay(function () {
        var $group_name = $('#groupNameInput');
        var name = $group_name.val();
        if (name.length > 2) {
            Dajaxice.publishing.validate_group_name(Dajax.process, {
                'group_name': $group_name.val()
            });

            $('#group-name-validation i').removeClass('icon-info-sign').addClass('icon-spinner icon-spin');
        }
    }, 1000);
});