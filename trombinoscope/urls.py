from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "trombinoscope"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("invite_users", views.invite_users_view, name="invite_users"),
    path("alumni", views.AlumniList.as_view(), name="alumni_list"),
    path("alumni/search_result", views.alumni_search_result, name="search"),
    path("update_profile", views.update_profile_view, name="update_profile"),
    path(
        "staffonly_update_profile/<id>/",
        views.staff_edit_profile,
        name="staff_edit_profile",
    ),
    path("set_password/<id>/", views.password_set_view, name="set_password"),
    path("contact", views.contact_view, name="contact"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
