from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView

# class IntroPageView(TemplateView):
#     def get_template_names(self):
#         return template_name

class IndexTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            q = request.META['QUERY_STRING']
            path = reverse('onepaper_intro')
            if q: 
                path += '?' + q
            return HttpResponseRedirect(path)
        else:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)

    def get_template_names(self):
        if self.request.user.is_authenticated:
            if settings.DEBUG:
                template_name = "index-dev.html"
            else:
                template_name = "index.html"
        return template_name

class IntroPageView(TemplateView):
    def get_template_names(self):
        template_name = "intro.html"
        return template_name

class EmailConfirmedView(TemplateView):
    def get_template_names(self):
        template_name = "account/email_confirmed.html"
        return template_name