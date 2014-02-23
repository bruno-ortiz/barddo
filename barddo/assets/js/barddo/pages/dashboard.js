
$(document).ready(function() {
    $(".collection-view").on("click", function() {
        var id = $(this).attr("data-id");
        Shards.shard.view.collection(function(shard_id, shard_data, parent) {
            $(shard_id).remove();
            $(parent).append(shard_data);
            $(shard_id).modal('show');
        }, {"collection_id": id});
    });


});