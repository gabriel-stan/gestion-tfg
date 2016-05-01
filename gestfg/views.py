from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect


class IndexView(TemplateView):
    template_name = 'index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):

        if self.request.user.is_authenticated() and self.request.user.is_admin:
            return super(DashboardView, self).dispatch(*args, **kwargs)

        return HttpResponseRedirect("/")
