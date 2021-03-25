from django.forms.widgets import Textarea
from django.db.models import TextField

from . import settings


class ToastUIWidget(Textarea):
    template_name = 'widgets/toastui.html'

    def get_context(self, name, value, attrs):
        attrs["style"] = "display: none;"
        context = super().get_context(name, value, attrs)
        context["widget"]["media"] = {
            "css": settings.TOASTUI_EDITOR_STYLE_PATH,
            "js": settings.TOASTUI_EDITOR_JS_PATH
        }
        return context


class ToastUIField(TextField):
    def formfield(self, **kwargs):
        opts = {
            'max_length': self.max_length,
            'widget': ToastUIWidget,
            **kwargs,
        }
        return super(TextField, self).formfield(**opts)
