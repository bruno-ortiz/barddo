/**
 * Easy way to create a delayed action, just pass your function callback
 */
var delay = (function(){
    var timer = 0;

    return function(callback, ms){
        clearTimeout (timer);
        timer = setTimeout(callback, ms);
    };
})();

/**
 * Display a temporary tooltip with given message over element
 * @param id of the element target to the tooltip
 * @param message to be displayed
 * @param delay to show the message
 * @param placement of the tooltip
 */
function error_tooltip(id, message, delay, placement) {

    delay = delay || 3000;
    placement = placement || "top";

    $(id).tooltip('destroy').tooltip({
        title:message,
        trigger: "manual",
        placement: placement,
        html: true
    }).tooltip('show');

    setTimeout(function() {
        $(id).tooltip('hide');
    }, delay);
}


/**
 * The fuelux wizar has no functionality to rewind the form, so
 * we create a temporary one ;)
 * @param $wizard the wizard object to be handled
 */
function wizardMoveFirst($wizard) {
    var $steps = $wizard.find('.wizard-steps li');
    var currentStep = $steps.filter('.active').index();

    for (var i = currentStep; i > 0; i--) {
        $wizard.wizard('previous');
    }
}