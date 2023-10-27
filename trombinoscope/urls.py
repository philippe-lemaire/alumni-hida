from django.urls import path


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
    path(
        "effacer-mon-profil", views.pre_delete_profile_view, name="pre_delete_profile"
    ),
    path(
        "effacer-mon-profil/confirmation",
        views.delete_profile_view,
        name="delete_profile",
    ),
]
