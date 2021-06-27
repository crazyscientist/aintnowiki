from django.conf import settings
from aintnowiki.settings import env

BRAND_HTML = env("BRAND_HTML", default="Ain't No Wiki")
TOASTUI_EDITOR_JS_PATH = getattr(
    settings, "ANW_TOASTUI_EDITOR_JS_PATH",
    ["https://uicdn.toast.com/editor/2.5.2/toastui-editor-all.min.js",
     "https://uicdn.toast.com/editor-plugin-uml/1.0.0/toastui-editor-plugin-uml.min.js"])
TOASTUI_EDITOR_STYLE_PATH = getattr(
    settings, "ANW_TOASTUI_EDITOR_STYLE_PATH",
    ["https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/codemirror.min.css",
     "https://uicdn.toast.com/editor/2.5.2/toastui-editor.min.css"])
TOASTUI_VIEWER_JS_PATH = getattr(
    settings, "ANW_TOASTUI_VIEWER_JS_PATH",
    ["https://uicdn.toast.com/editor/2.5.2/toastui-editor-viewer.min.js",
     "https://uicdn.toast.com/editor-plugin-uml/1.0.0/toastui-editor-plugin-uml.min.js"])
TOASTUI_VIEWER_STYLE_PATH = getattr(
    settings, "ANW_TOASTUI_VIEWER_STYLE_PATH",
    ["https://uicdn.toast.com/editor/2.5.2/toastui-editor-viewer.min.css"]
)
PLANTUML_RENDERER_URL = env("PLANTUML_RENDERER_URL",
                            default="http://www.plantuml.com/plantuml/svg/")
VUE_JS_PATH = getattr(settings, "ANW_VUE_JS_PATH", ["https://cdn.jsdelivr.net/npm/vue@2"])
