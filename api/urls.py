from django.urls import path
from . import views
urlpatterns = [
	# path('', views.ApiOverview, name='home'),
	path('posts/',views.post_list,name = 'post-list'),
	path('posts/<int:postId>/',views.post_detail,name = 'post-detail'),
	path('category/',views.category_list, name = 'category-list'),
	path('category/<int:categoryId>/',views.category_detail, name = 'category-detail'),
	path('users/',views.user_list, name = 'user-list'),
	path('users/<int:userId>/',views.user_detail, name = 'user-detail'),
	path('bodypost/',views.body_list, name = 'body-list'),
	path('bodypost/<str:bodyId>/',views.body_detail, name = 'body-detail'),
	path('login/',views.login, name = 'login'),
	# path('logout/',knox_views.LogoutView.as_view(), name = 'logout'),
]
