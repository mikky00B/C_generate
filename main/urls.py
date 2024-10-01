from django.urls import path
from .views import generate_content, signup, content_history, export_pdf, analytics

urlpatterns = [
    path("generate/", generate_content, name="generate_content"),
    path("signup/", signup, name="signup"),
    path("history/", content_history, name="content_history"),
    path("export_pdf/<int:content_id>/", export_pdf, name="export_pdf"),
    path("analytics/", analytics, name="analytics"),
]
