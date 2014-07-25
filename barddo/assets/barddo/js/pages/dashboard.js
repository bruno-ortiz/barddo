Dropzone.autoDiscover = false;

function sortable_image_upload(target, preview_container, existing_data) {

    existing_data = existing_data || null;

    /**
     * Work pages dropzone
     */
    var dropzoned = $(target).dropzone({
        paramName: "file", // The name that will be used to transfer the file
        maxFilesize: 1.5, // MB,
        maxFiles: 300, // TODO: need this limit
        parallelUploads: 1,
        uploadMultiple: false,

        addRemoveLinks: false,
        dictResponseError: 'Error while uploading file!',
        dictDefaultMessage: "Drop your work pages here to upload! (Or Click)",

        //change the previewTemplate to use Bootstrap progress bars
        previewTemplate: "<div class=\"dz-preview dz-file-preview\">\n  <div class=\"dz-details\">\n    <div class=\"dz-filename\"><span data-dz-name></span></div>\n    <div class=\"dz-size\" data-dz-size></div>\n    <img data-dz-thumbnail />\n  </div>\n  <div class=\"progress progress-small progress-striped active\"><div class=\"progress-bar progress-bar-success\" data-dz-uploadprogress></div></div>\n  <div class=\"dz-success-mark\"><span></span></div>\n  <div class=\"dz-error-mark\"><span></span></div>\n  <div class=\"dz-error-message\"><span data-dz-errormessage></span></div>\n</div>",
        previewsContainer: preview_container,
        init: function () {
            this.on("addedfile", function (file) {
                $('.dz-message').hide();

                var removeButton = Dropzone.createElement('<a class="dz-remove">Remove Page</a>');

                // Capture the Dropzone instance as closure.
                var _this = this;

                // Listen to the click event
                removeButton.addEventListener("click", function (e) {
                    e.preventDefault();
                    e.stopPropagation();

                    var selectedIndex = $(this).closest("div.dz-preview").index();
                    var work_id = $(target).attr('data-id');

                    $(".work-action-overlay").fadeIn('fast');

                    $.ajax({
                        type: "POST",
                        url: "/work/" + work_id + "/page/" + selectedIndex + "/remove",

                        headers: {
                            "X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').val()
                        },

                        success: function (data) {
                            _this.removeFile(file);
                            $(".work-action-overlay").fadeOut('fast');
                        },

                        error: function (data) {
                            alert('error ;(');
                        },

                        timeout: function (data) {
                            alert('no response ;(');
                        }
                    });
                });

                // Add the button to the file preview element.
                file.previewElement.appendChild(removeButton);
            });

            this.on("removedfile", function (file) {
                if (!$(".dz-preview").length) {
                    $('.dz-message').show();
                }
            });

            this.on("processing", function (file) {
                this.options.url = "/work/page/upload/" + $(target).attr('data-id');
            });

            if (existing_data != null) {
                var drop = this;

                $(existing_data).each(function () {
                    var file_name = $(this).text();
                    var file_size = $(this).attr("data-size");
                    var file_url = $(this).attr("data-url");

                    // Create the mock file:
                    var mockFile = { name: file_name, size: file_size };

                    // Call the default addedfile event handler
                    drop.emit("addedfile", mockFile);

                    // And optionally show the thumbnail of the file:
                    drop.emit("thumbnail", mockFile, file_url);

                    // If you use the maxFiles option, make sure you adjust it to the
                    // correct amount:
                    var existingFileCount = 1; // The number of files already uploaded
                    drop.options.maxFiles = drop.options.maxFiles - existingFileCount;
                });

                $(".progress").hide();
            }
        }
    });

    var sort_from_index = -1;

    $(preview_container).sortable({
        placeholder: "placeholder",
        forcePlaceholderSize: true,
        start: function (event, ui) {
            sort_from_index = ui.item.index();
        },

        stop: function (event, ui) {
            var to_index = ui.item.index()

            if (sort_from_index != to_index) {
                var work_id = $(target).attr('data-id');
                //alert("from index " + sort_from_index + " to " + to_index);
                $(".work-action-overlay").fadeIn('fast');

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
                        $(".work-action-overlay").fadeOut('fast');
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

    $(preview_container).disableSelection();
    return dropzoned;
}

$(document).ready(function () {
    $(".collection-view").on("click", function () {
        var id = $(this).attr("data-id");

        Shards.modal.work(function (shard_id, shard_data, parent) {
            $(shard_id).remove();
            $(parent).append(shard_data);
            $(shard_id).modal('show');

            sortable_image_upload('#edit-work-upload', "#edit-work-files-preview", "#work-file-list li");

        }, {"work_id": id});
    });

    sortable_image_upload('#new_work_upload', "#files-preview");
});