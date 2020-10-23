from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='Hydroxychloroquine-home'),
    path('home/', views.home, name='Hydroxychloroquine-home'),
    path('account/', views.account,  name='Hydroxychloroquine-account'),
    path('forgotPassword/', views.forgotPassword,  name='Hydroxychloroquine-forgotPassword'),
    path('index/', views.index,  name='Hydroxychloroquine-index'),
    path('login/', views.login,  name='Hydroxychloroquine-login'),
    path('reportTest/', views.reportTest,  name='Hydroxychloroquine-reportTest'),
    path('selectBuildings/', views.selectBuildings,  name='Hydroxychloroquine-selectBuildings'),
    path('signup/', views.signup,  name='Hydroxychloroquine-signup'),

    path('test_about/', views.test_about, name='Hydroxychloroquine-test_about'),
    path('test_base/', views.test_base,  name='Hydroxychloroquine-test_base'),
    path('test_home/', views.test_home,  name='Hydroxychloroquine-test_home'),
]
