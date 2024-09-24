from django.urls import path

from kitchen.views import (
    DishListView,
    DishTypeCreateView,
    CookListView,
    CookCreateView,
    DishCreateView,
    DishUpdateView,
    DishDeleteView,
    DishTypeListView,
    CookUpdateView,
    DishTypeDeleteView,
    DishTypeUpdateView,
    HomeView,
    DishDetailView,
    CookDetailView,
    CookDeleteView
)

app_name = 'kitchen'

urlpatterns = [
    path('dish/', DishListView.as_view(), name='dish-list'),
    path('dish/create/', DishCreateView.as_view(), name='dish-create'),
    path('dish/<int:pk>/update/', DishUpdateView.as_view(), name='dish-update'),
    path('dish/<int:pk>/delete/', DishDeleteView.as_view(), name='dish-delete'),
    path('dish_type/', DishTypeListView.as_view(), name='dish-type-list'),
    path('dish_type/create/', DishTypeCreateView.as_view(), name='dish-type-create'),
    path('dish_type/<int:pk>/update/', DishTypeUpdateView.as_view(), name='dish-type-update'),
    path('dish_type/<int:pk>/delete/', DishTypeDeleteView.as_view(), name='dish-type-delete'),
    path('dish/<int:pk>/', DishDetailView.as_view(), name='dish-detail'),
    path('cook/<int:pk>/', CookDetailView.as_view(), name='cook-detail'),
    path('cook/', CookListView.as_view(), name='cook-list'),
    path('cook/create/', CookCreateView.as_view(), name='cook-create'),
    path('cook/<int:pk>/update/', CookUpdateView.as_view(), name='cook-update'),
    path('cook/<int:pk>/delete/', CookDeleteView.as_view(), name='cook-delete'),
    path('', HomeView.as_view(), name='home'),
]
