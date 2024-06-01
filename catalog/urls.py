from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet, PublisherViewSet, BorrowerViewSet, LoanViewSet, UserLoginView

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'publishers', PublisherViewSet)
router.register(r'borrowers', BorrowerViewSet)
router.register(r'loans', LoanViewSet)

urlpatterns = [
    path('login/', UserLoginView.as_view()),
    path('', include(router.urls)),
]
