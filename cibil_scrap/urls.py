from django.urls import path
from .views import *

app_name = "cibil"

urlpatterns = [
    path("home/", home, name="home"),
    path("", dropdown_form_view, name="dropdown_form_view"),
    path("cibil_search/", cibil_search, name="cibil_search"),
    path("suit_cibil_search", suit_cibil_search, name="suit_cibil_search"),
]
