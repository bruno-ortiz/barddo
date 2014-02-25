{{ name }}: {
    {% include "shards/shards.functions.js" %}
    {% with parent_foorloop=forloop %}
    {% for name, sub_module in module.submodules.items %}
    {% with filename="shards/shards.modules.js" module=sub_module %}
    {% include filename %}
    {% endwith %}
    {% if not forloop.last %},{% endif %}
    {% endfor %}
}
{% endwith %}