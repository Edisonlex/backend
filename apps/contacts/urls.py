# urls.py
from django.urls import path
from .views import ContactCreateView, NewsletterSubscriptionView

urlpatterns = [
    path('', ContactCreateView.as_view()),
    path('newsletter/', NewsletterSubscriptionView.as_view()),
]
