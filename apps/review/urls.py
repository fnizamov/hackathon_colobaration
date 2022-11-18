from rest_framework import routers
from .views import CommentView

router = routers.DefaultRouter()
router.register('comments', CommentView, 'comment')
urlpatterns = [

]
urlpatterns += router.urls