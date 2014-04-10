function send_feedback() {
    var form_data = $("#feedbackForm").serialize();
    Dajaxice.feedback.send_feedback(Dajax.process, {"form_data": form_data});

    $("button#send-feedback").prop('disabled', true);
    $("button#send-feedback").html("<i class='icon-spinner icon-spin'/> Sending...");
}

function callback_feedback_ok(title, message) {
    gritterSuccess(title, message);
    $("#feedbackModal").modal("hide");
    $("button#send-feedback").html("<i class='icon-ok'/> Sent!");
}

function callback_feedback_error() {
    $("button#send-feedback").prop('disabled', false);
    $("button#send-feedback").html("<i class='icon-ok'/> Try Again!");
}