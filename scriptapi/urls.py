from django.urls import path
from scriptapi.auth import login_user, register_user, protected_view, logout_user
from scriptapi.views import (
    upload_transcript,
    get_transcripts,
    create_parsed_file,
    get_user_files,
    save_parsed_file,
    delete_transcript,
    get_parsed_file,
    delete_parsed_file,
    rename_transcript,
    get_keyword_stats,
    rename_parsed_file,
    get_files_by_keyword,
)

urlpatterns = [
    path("login", login_user),
    path("register", register_user),
    path("logout", logout_user),
    path("protected", protected_view),
    path("upload", upload_transcript),
    path("transcripts", get_transcripts),
    path("parsed", create_parsed_file),
    path("files", get_user_files),
    path("files/save", save_parsed_file),
    path("transcripts/<int:pk>/delete", delete_transcript),
    path("files/<int:pk>", get_parsed_file),
    path("files/<int:pk>/delete", delete_parsed_file),
    path("transcripts/<int:pk>/rename", rename_transcript),
    path("keywords", get_keyword_stats),
    path("files/<int:file_id>/rename", rename_parsed_file),
    path("files/by_keyword/<str:keyword>", get_files_by_keyword),
]


# from django.urls import path
# from . import auth

# urlpatterns = [
#     path("login", auth.login_user),
#     path("register", auth.register_user),
# ]
