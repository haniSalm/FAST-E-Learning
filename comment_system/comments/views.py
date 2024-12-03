from rest_framework import status, viewsets  # Import viewsets here
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Comment, Course, Rating, Assignment, Alumni, Quizz, PastPaper, CourseMaterial
from .serializers import (
    UserSerializer, 
    CommentSerializer, 
    CourseSerializer, 
    CourseDetailSerializer, 
    RatingSerializer,
    AssignmentSerializer,
    QuizzSerializer,
    PastPaperSerializer,
    CourseMaterialSerializer
)
from rest_framework.parsers import MultiPartParser, FormParser  # Allow file uploads
from rest_framework import generics

# Constants
COURSE_NOT_FOUND_MESSAGE = {"error": "Course not found"}
STATUS_NOT_FOUND = status.HTTP_404_NOT_FOUND
RATING_ERROR_MESSAGE = {"error": "Rating must be between 1 and 5"}
ALREADY_RATED_ERROR_MESSAGE = {"error": "You have already rated this course"}

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            comments = Comment.objects.filter(course=course).order_by("-timestamp")
            if not comments.exists():
                return Response({"message": "No comments yet."}, status=status.HTTP_200_OK)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response(COURSE_NOT_FOUND_MESSAGE, status=STATUS_NOT_FOUND)

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, course=course)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            return Response(COURSE_NOT_FOUND_MESSAGE, status=STATUS_NOT_FOUND)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    parser_classes = (MultiPartParser, FormParser)  # Allow file uploads for Course images

    def perform_create(self, serializer):
        serializer.save()


class CourseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            rating_value = request.data.get('rating')

            if rating_value not in [1, 2, 3, 4, 5]:
                return Response(RATING_ERROR_MESSAGE, status=status.HTTP_400_BAD_REQUEST)

            # Check if the user has already rated this course
            if Rating.objects.filter(course=course, user=request.user).exists():
                return Response(ALREADY_RATED_ERROR_MESSAGE, status=status.HTTP_400_BAD_REQUEST)

            # Save the rating directly without assigning to a variable
            Rating.objects.create(course=course, user=request.user, rating=rating_value)
            return Response({"message": "Rating submitted successfully!"}, status=status.HTTP_201_CREATED)
        except Course.DoesNotExist:
            return Response(COURSE_NOT_FOUND_MESSAGE, status=STATUS_NOT_FOUND)



class AssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Assignment.objects.filter(course_id=course_id)


class AssignmentCreateView(generics.CreateAPIView):
    serializer_class = AssignmentSerializer
    parser_classes = (MultiPartParser, FormParser)


class AssignmentDeleteView(APIView):
    def delete(self, request, pk):
        try:
            assignment = Assignment.objects.get(pk=pk)
            assignment.delete()
            return Response({"message": "Assignment deleted successfully"}, status=status.HTTP_200_OK)
        except Assignment.DoesNotExist:
            return Response({"error": "Assignment not found"}, status=STATUS_NOT_FOUND)


class UserStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Check if the current user is an alumni
        is_alumni = Alumni.objects.filter(email=request.user.email).exists()
        return Response({"is_alumni": is_alumni})


class QuizzListView(generics.ListAPIView):
    serializer_class = QuizzSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Quizz.objects.filter(course_id=course_id)


class QuizzCreateView(generics.CreateAPIView):
    serializer_class = QuizzSerializer
    parser_classes = (MultiPartParser, FormParser)


class QuizzDeleteView(APIView):
    def delete(self, request, pk):
        try:
            quizz = Quizz.objects.get(pk=pk)
            quizz.delete()
            return Response({"message": "Quizz deleted successfully"}, status=status.HTTP_200_OK)
        except Quizz.DoesNotExist:
            return Response({"error": "Quizz not found"}, status=STATUS_NOT_FOUND)


class PastPaperListView(generics.ListAPIView):
    serializer_class = PastPaperSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return PastPaper.objects.filter(course_id=course_id)


class PastPaperCreateView(generics.CreateAPIView):
    serializer_class = PastPaperSerializer
    parser_classes = (MultiPartParser, FormParser)


class PastPaperDeleteView(APIView):
    def delete(self, request, pk):
        try:
            pastpaper = PastPaper.objects.get(pk=pk)
            pastpaper.delete()
            return Response({"message": "Past paper deleted successfully"}, status=status.HTTP_200_OK)
        except PastPaper.DoesNotExist:
            return Response({"error": "Past paper not found"}, status=STATUS_NOT_FOUND)


class CourseMaterialListView(generics.ListAPIView):
    serializer_class = CourseMaterialSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return CourseMaterial.objects.filter(course_id=course_id)


class CourseMaterialCreateView(generics.CreateAPIView):
    serializer_class = CourseMaterialSerializer
    parser_classes = (MultiPartParser, FormParser)


class CourseMaterialDeleteView(APIView):
    def delete(self, request, pk):
        try:
            coursematerial = CourseMaterial.objects.get(pk=pk)
            coursematerial.delete()
            return Response({"message": "Course material deleted successfully"}, status=status.HTTP_200_OK)
        except CourseMaterial.DoesNotExist:
            return Response({"error": "Course material not found"}, status=STATUS_NOT_FOUND)
