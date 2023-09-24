from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "trombinoscope"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("invite_users", views.invite_users_view, name="invite_users"),
    path("alumni", views.alumni_list_view, name="alumni_list"),
    path("update_profile/<id>/", views.update_profile_view, name="update_profile"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
