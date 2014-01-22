

/**
 * A delayed function to use when need the user interaction
 */
var delay = (function(){
  var timer = 0;

  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();


function callback_collection_name_is_not_avaliable() {
    $("#collection-name-group").removeClass("has-success has-info").addClass("has-error")
    $("#collection-name-group i").removeClass().addClass("icon-exclamation-sign")
    $("#collection-next").prop('disabled', true);
}

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
$('#collection-name-validation').keyup(function() {
    delay(function(){
        Dajaxice.core.validate_unique_collection(Dajax.process, {
            'collection_name': $('#collection-name-validation').val()
        });

        $('#collection-name-group i').removeClass('icon-info-sign').addClass('icon-spinner icon-spin');
    }, 1000);
});