from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin  # Import admin from django.contrib
from bloggingapp import settings
from gallery import views

urlpatterns = [
                  path('', views.post_list, name='post_list'),
                  path('signin/', views.signin, name="signin"),
                  path('signout', views.signout, name="signout"),
                  path('post/<int:pk>/', views.post_detail, name='post_detail'),
                  path('search', views.search, name="search"),
                  path('category/<int:category_id>/', views.category_posts, name='category_posts'),
                  path('post/new/', views.post_new, name='post_new'),
                  path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
                  path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
                  path('admin/', admin.site.urls),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
