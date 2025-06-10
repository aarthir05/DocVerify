from django.urls import path
from .views import signup_view, upload_document, list_documents, verify_document, delete_document
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('api/signup/', signup_view, name='signup'),
    path('api/upload/', upload_document, name='upload_document'),
    path('api/documents/<int:user_id>/', list_documents, name='list_documents'),
    path('api/verify/<int:doc_id>/', verify_document, name='verify_document'),
    path('api/delete/<int:doc_id>/', delete_document, name='delete_document'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
