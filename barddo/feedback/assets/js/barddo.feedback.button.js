$(document).ready(function () {
    $("#feedbackButton").on("click", function () {
        Shards.feedback(function (shard_id, shard_data, parent) {
            $(shard_id).remove();
            $(parent).append(shard_data);
            $(shard_id).modal('show');
        });
    });
});