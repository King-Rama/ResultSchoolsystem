from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = 'home/index.html'


class UploadError(TemplateView):
    template_name = 'info.html'


class UploadSuccess(TemplateView):
    template_name = 'success.html'


