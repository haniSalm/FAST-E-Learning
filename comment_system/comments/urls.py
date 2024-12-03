from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignupView, LoginView, CommentView, CourseViewSet, CourseDetailView,AssignmentListView,AssignmentCreateView,AssignmentDeleteView
from .views import UserStatusView
from .views import PastPaperListView,PastPaperDeleteView,PastPaperCreateView
from .views import QuizzCreateView,QuizzDeleteView,QuizzListView
from .views import CourseMaterialCreateView,CourseMaterialDeleteView,CourseMaterialListView
# Initialize the router
router = DefaultRouter()
router.register('courses', CourseViewSet, basename='course')

# Define the urlpatterns
urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('comments/course/<int:course_id>/', CommentView.as_view()),  # Comments for a specific course
    path('course/<int:course_id>/', CourseDetailView.as_view()),  # Course Detail API
    path('course/<int:course_id>/rate/', CourseDetailView.as_view()),  # Rating submission API

    path('courses/<int:course_id>/assignments/', AssignmentListView.as_view(), name='list_assignments'),
    path('courses/<int:course_id>/assignments/create/', AssignmentCreateView.as_view(), name='create_assignment'),
    path('assignments/<int:pk>/delete/', AssignmentDeleteView.as_view(), name='assignment-delete'),

    path('user/status/', UserStatusView.as_view(), name='user-status'),

     path('courses/<int:course_id>/quizzes/', QuizzListView.as_view(), name='list_quizz'),
    path('courses/<int:course_id>/quizzes/create/', QuizzCreateView.as_view(), name='create_quizz'),
    path('quizzes/<int:pk>/delete/', QuizzDeleteView.as_view(), name='quizz-delete'),


     path('courses/<int:course_id>/pastpapers/', PastPaperListView.as_view(), name='list_pastpaper'),
    path('courses/<int:course_id>/pastpapers/create/', PastPaperCreateView.as_view(), name='create_pastpaper'),
    path('pastpapers/<int:pk>/delete/', PastPaperDeleteView.as_view(), name='pastpaper-delete'),


path('courses/<int:course_id>/coursematerials/', CourseMaterialListView.as_view(), name='list_coursematerial'),
    path('courses/<int:course_id>/coursematerials/create/', CourseMaterialCreateView.as_view(), name='create_coursematerial'),
    path('coursematerials/<int:pk>/delete/', CourseMaterialDeleteView.as_view(), name='coursematerial-delete'),


    path('', include(router.urls)),
]