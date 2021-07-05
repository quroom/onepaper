from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

# class IntroPageView(TemplateView):
#     def get_template_names(self):
#         return template_name

class IndexTemplateView(TemplateView):
    def get_template_names(self):
        if self.request.user.is_authenticated:
            if settings.DEBUG:
                template_name = "index-dev.html"
            else:
                template_name = "index.html"
        else:
            template_name = "intro.html"
        return template_name