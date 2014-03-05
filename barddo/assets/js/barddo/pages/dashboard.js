Dropzone.autoDiscover = false;

$(document).ready(function () {
    $(".collection-view").on("click", function () {
        var id = $(this).attr("data-id");
        Shards.modal.collection(function (shard_id, shard_data, parent) {
            $(shard_id).remove();
            $(parent).append(shard_data);
            $(shard_id).modal('show');
        }, {"collection_id": id});
    });

    /**
     * Work pages dropzone
     */
    $(".dropzone").dropzone({
        paramName: "file", // The name that will be used to transfer the file
        maxFilesize: 0.5, // MB

        addRemoveLinks: true,
        dictResponseError: 'Error while uploading file!',

        //change the previewTemplate to use Bootstrap progress bars
        previewTemplate: "<div class=\"dz-preview dz-file-preview\">\n  <div class=\"dz-details\">\n    <div class=\"dz-filename\"><span data-dz-name></span></div>\n    <div class=\"dz-size\" data-dz-size></div>\n    <img data-dz-thumbnail />\n  </div>\n  <div class=\"progress progress-small progress-striped active\"><div class=\"progress-bar progress-bar-success\" data-dz-uploadprogress></div></div>\n  <div class=\"dz-success-mark\"><span></span></div>\n  <div class=\"dz-error-mark\"><span></span></div>\n  <div class=\"dz-error-message\"><span data-dz-errormessage></span></div>\n</div>",
        previewsContainer: "#files-preview",
        init: function () {
            this.on("addedfile", function (file) {
                $('.dz-message').hide();
            });

            this.on("processing", function (file) {
                this.options.url = "/work/page/upload/" + $('#new_work_upload').attr('data-id');
            });
        }
    });

    var sort_from_index = -1;

    $("#files-preview").sortable({
        placeholder: "placeholder",
        forcePlaceholderSize: true,
        start: function (event, ui) {
            sort_from_index = ui.item.index();
        },

        stop: function (event, ui) {
            var to_index = ui.item.index()

            if (sort_from_index != to_index) {
                var work_id = $("#new_work_upload").attr('data-id');
                //alert("from index " + sort_from_index + " to " + to_index);

                $.ajax({
                    type: "POST",
                    url: "/work/page/order/" + work_id,
                    data: {
                        position_from: sort_from_index,
                        position_to: to_index
                    },

                    headers: {
                        "X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').val()
                    },

                    success: function (data) {
                        //alert('done');
                    },

                    error: function (data) {
                        alert('error ;(');
                    },

                    timeout: function (data) {
                        alert('no response ;(');
                    }
                })
            }
        }
    });

    $("#files-preview").disableSelection();
});