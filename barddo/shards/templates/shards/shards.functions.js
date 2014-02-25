{% for function_name, function in module.callables.items %}
{{ function_name }}: function (callback, argv, parent) {
    parent = parent || "body";
    return Shards.load('{{ function.name }}', parent, callback, argv);
}{% if not forloop.last or top or module.submodules %},{% endif %}
{% endfor %}