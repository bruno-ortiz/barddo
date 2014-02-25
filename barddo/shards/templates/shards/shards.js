{% load url from future %}
var Shards = {

    {% with module=shard_manager.modules top='top' %}
    {% include "shards/shards.functions.js" %}
    {% endwith %}

    {% for name, module in shard_manager.modules.submodules.items %}
    {% include "shards/shards.modules.js" %},
    {% endfor %}

    load: function (function_name, parent, callback, argv) {
    $.ajax({
        url: "{% url 'shards-endpoint' %}" + function_name + "/",
        success: function (shard_data) {
            gritterClear();

            var shard_id = "#" + $(shard_data).attr('id');
            callback.call(this, shard_id, shard_data, parent);
        },
        dataType: 'html',
        data: argv,
        type: "POST",
        headers: {
            'X-CSRFToken': Shards.get_cookie('csrftoken')
        },

        // TODO: this should be generic
        timeout: function () {
            //gritterClear();
            gritterError("Request Error", "Unfortunately, your request timed out!");
        },

        error: function () {
            // TODO: log these errors
            //gritterClear();
            gritterError("Request Error", "Unfortunately, your request has finished with errors!");
        },

        beforeSend: function () {
            gritterCenter("", '<center><i class="icon-spinner icon-spin white icon-3x"></i></center>', true)
        }
    });

    return false;
},

get_cookie: function (name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].toString().replace(/^\s+/, "").replace(/\s+$/, "");
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
},
};

window['Shards'] = Shards;