from django.contrib import admin
from django.urls import path

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('interpolate/', views.InterpolationView.as_view({'post': 'post'}), name='interpolate1'),
    path('interpolate2/', views.InterpolationView.as_view({'post': 'post'}), name='interpolate2'),
    path('outlier/', views.OutlierDetectionView.as_view({'post': 'post'}), name='outlier'),
    path('unbalance/', views.UnbalancedManagingView.as_view({'post': 'post'}), name='unbalance'),
]
