from urllib import request
from django import template
from django.contrib.sites.shortcuts import get_current_site
import environ
import json
from config import settings
from django.utils.safestring import mark_safe
from django.templatetags.static import static

register = template.Library()


@register.simple_tag(takes_context=True)
def vite(context) -> str:
    env = environ.Env()
    vite_port = env("VITE_PORT")
    request = context.get("request")
    scheme = request.scheme
    domain = get_current_site(request).domain

    manifest_path = settings.STATIC_ROOT / "manifest.json"

    if not settings.DEBUG and not manifest_path.exists():
        raise Exception("Error: manifest.json not found.")

    if settings.DEBUG:
        return mark_safe(
            f"""<script type="module" src="{scheme}://{domain}:{vite_port}/@vite/client"></script>
            <script type="module" src="{scheme}://{domain}:{vite_port}{settings.VITE_SRC}js/main.js"></script>"""
        )
    else:
        manifest = json.loads(manifest_path.read_text())
        css_file = static("ui/" + manifest["src/js/main.css"]["file"])
        js_file = static("ui/" + manifest["src/js/main.js"]["file"])

        return mark_safe(
            f"""<link rel="stylesheet" type="text/css" href="{css_file}">
            <script type="module" src="{js_file}"></script>"""
        )
