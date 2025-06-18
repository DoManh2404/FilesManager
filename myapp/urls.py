from myapp.views import views_filesharing, views_login, views_test
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

urlpatterns = [
    # login urls
    path('signup/', views_login.SignUpView.as_view(), name='signup'),
    path('login/', views_login.LoginView.as_view(), name='login'),
    path('logout/', views_login.LogoutView.as_view(), name='logout'),
    path('home/', views_login.HomeView.as_view(), name='home'),
    # filesharing urls
    path('files/', views_filesharing.FileListView.as_view(), name='file_list'),
    path('files/upload/', views_filesharing.FileUploadView.as_view(), name='file_upload'),
    path('files/download/<str:file_name>/', views_filesharing.FileDownloadView.as_view(), name='file_download'),
    path('files/delete/', views_filesharing.FileDeleteView.as_view(), name='file_delete'),
    path('files/search/', views_filesharing.FileSearchView.as_view(), name='file_search'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
