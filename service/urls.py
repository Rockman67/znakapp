from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.urls import include


urlpatterns = [
    path('', views.index, name='homepage'),
    path('price-list/', views.price_list, name='price'),
    path('price-cabinet/<str:user_id>', views.price_cabinet, name='price-cabinet'),
    path('partner/<str:user_id>', views.partner, name='partner'),
    path('user_history/<str:user_id>', views.history, name='history'),
    path('user_history/<str:user_id>/download/<str:element_id>', views.download_images, name='download_images'),
    path('user-history/<str:user_id>/<str:element_id>', views.open_photos, name='open_photos'),
    path('user-profile/<str:user_id>', views.profile, name='profile'),
    path('info_page/<str:token>/', views.confirm_email, name='confirm_email'),
    path('logout/', views.user_logout, name='logout'),
    path('cabinet/<str:user_id>', views.cabinet, name='cabinet'),
    path('partner/<str:referal>', views.partner, name='partner-url'),
    path('telegram-bot-info',views.tg_info,name='tg_info'),
    path('api-info', views.api_info, name='api_info'),
    path('api-cabinet/<str:user_id>', views.api_cabinet, name='api_cabinet'),
    path('process_webhook/',views.process_webhook,name='process_webhook')
]