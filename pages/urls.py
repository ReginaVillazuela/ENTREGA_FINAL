from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_pages, name='pages_list'),
    path('categories/', views.CategorySelectionView.as_view(), name='category_selection'),
    path('crear/', views.PageCreateView.as_view(), name='page_create'),
    path('<int:pk>/', views.page_detail, name='page_detail'),
    path('<int:pk>/editar/', views.PageUpdateView.as_view(), name='page_edit'),
    path('<int:pk>/borrar/', views.PageDeleteView.as_view(), name='page_delete'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/rate/', views.page_rate, name='page_rate'),
    path('about/', views.about_view, name='about'),
    path('list/', views.list_pages, name='list_pages'),
]

