from django import template
from django.contrib.admin.options import json
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag("ui/base_component.html", takes_context=True)
def ui_include(context, template: str, ctx: str = "", **kwargs):
    """Insert template in other template.

    Args:
        context (RequestContext): Request context
        template (string): Path to template file
        from_ctx (str, optional): By default all request context is passed, but this
        can be more selective, is you specify context keys in this argument.
        Keys must be separated by commas. Defaults to ''.

    Returns:
        dict: Template context.
    """

    _ctx: dict = {}

    if ctx:
        from_ctx_splitted = [i.strip() for i in ctx.split(",")]
        _ctx = {key: context.get(key, None) for key in from_ctx_splitted}
    else:
        _ctx = context.flatten()

    return {
        **_ctx,
        **kwargs,
        "template": template,
    }


@register.inclusion_tag("ui/form/field.html")
def form_field(field, label_attrs="", field_attrs=""):
    """Render a form field. Field must have a widget."""
    label_attrs_str = ""
    label_class = ""

    if label_attrs:
        label_attrs = json.loads(label_attrs)
        label_attrs_str = ""

        for key, value in label_attrs.items():
            if key == "class":
                label_class = value
            label_attrs_str += f' {key}="{value}"'

        label_attributes = label_attrs_str.strip()

    if field_attrs:
        field_attrs = json.loads(field.attrs)
        field.widget.attr.update(field_attrs)

    field_attrs = json.loads(field_attrs)

    return {
        "field": field,
        "label_attributes": label_attrs_str,
        "label_class": label_class,
    }


@register.inclusion_tag("ui/form/field_reverse.html")
def form_field_inline(field, reverse=False):
    return {"field": field, "reverse": reverse}


@register.inclusion_tag("ui/icons/tag_icon.html")
def icon(icon, width=6, height=6, extra_class="", attrs=""):
    """Render an icon."""

    icon = icon.replace(".", "/")
    template = f"ui/icons/{icon}.html"

    attrs_splitted = attrs.split(" ")

    _attrs = ""

    for attr in attrs_splitted:
        [key, value] = attr.split("=")
        if key == "class":
            extra_class += f" {value}"
        else:
            _attrs += f' {key}="{value}"'

    _attrs = mark_safe(_attrs.strip().replace("'", '"')) 
    extra_class = mark_safe(extra_class.strip())

    return {
        "icon": icon,
        "width": width,
        "height": height,
        "extra_class": extra_class,
        "attrs": attrs,
        "template": template,
    }
