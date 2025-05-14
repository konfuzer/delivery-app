from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from deliveries.views import report_dashboard


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('deliveries.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reports/', report_dashboard, name='report_dashboard'),
    path('', report_dashboard, name='index'),
]