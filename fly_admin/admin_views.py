from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path


class AdminViewsMixin(admin.AdminSite):

    def each_context(self, request):
        """Returns a dictionary of context variables 
        to be passed to the each template."""

        context = super().each_context(request)

        return context

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path("example/", self.admin_view(self.example_admin_view), name="example"),
        ]

        return custom_urls + urls


    def example_admin_view(self, request):
        request.current_app = self.name
        context: dict = self.each_context(request)

        return TemplateResponse(request, "examples/admin_example.html", context)
