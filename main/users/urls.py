from django.conf.urls import url,include
from users.views import dashboard, register
from . import views
from properties import views as viewsp
urlpatterns = [
    url(r"accounts/", include("django.contrib.auth.urls")),
    url("dashboard/", viewsp.news_list, name="dashboard"),
    url(r"register/", views.register, name="register"),
]
