from django.urls import path
from .views import PasteAnalyticsView, PasteView

urlpatterns = [
    path('', PasteView.as_view()),
    path('<str:key>/', PasteView.as_view()),
    path('analytics', PasteAnalyticsView.as_view()),
    path('analytics/<str:key>', PasteAnalyticsView.as_view()),
]