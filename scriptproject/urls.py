from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("scriptapi.urls")),
]


# from django.contrib import admin
# from django.urls import include, path
# from rest_framework import routers

# router = routers.DefaultRouter(trailing_slash=False)

# urlpatterns = [
#     # path("", include(router.urls)),
#     path("api/", include("scriptapi.urls")),
# ]
