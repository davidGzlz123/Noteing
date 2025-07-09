from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet, CheckboxItemViewSet, NumberedItemViewSet
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r'notes', NoteViewSet)
router.register(r'checkboxes', CheckboxItemViewSet)
router.register(r'numbers', NumberedItemViewSet)

urlpatterns = [
  path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
