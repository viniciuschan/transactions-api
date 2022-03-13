from django.conf.urls import include
from django.contrib import admin
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path
from rest_framework_swagger.views import get_swagger_view

ping_view = lambda request: HttpResponse("pong!")


def project_index(request):
    return TemplateResponse(request, "index.html")


swagger_view = get_swagger_view(title="Transactions API")
swagger_url = [path(r"v1/docs", swagger_view, name="schema")]

urlpatterns = [
    path("", project_index),
    path("v1/", include("src.urls")),
    path("admin/", admin.site.urls),
    path("ping/", ping_view),
]

urlpatterns.extend(swagger_url)
