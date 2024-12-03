from rest_framework import serializers
from .models import CustomUser  # Import the custom user model
from .models import Comment
from .models import Course
from .models import Rating
from .models import Assignment
from .models import Quizz
from .models import PastPaper
from .models import CourseMaterial

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Use the custom user model
        fields = ['id', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
            'email': {'required': True},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class CommentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)  # Add course title

    class Meta:
        model = Comment
        fields = ['id', 'text', 'timestamp', 'user_email', 'course_title']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'created_at', 'image']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'course', 'user', 'rating']

class CourseDetailSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    number_of_ratings = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'created_at', 'image', 'ratings', 'average_rating', 'number_of_ratings']

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings:
            return sum(rating.rating for rating in ratings) / len(ratings)
        return 0

    def get_number_of_ratings(self, obj):
        return obj.ratings.count()


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'image', 'file', 'course']


class QuizzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quizz
        fields = ['id', 'title', 'description', 'image', 'file', 'course']

class PastPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastPaper
        fields = ['id', 'title', 'description', 'image', 'file', 'course']

class CourseMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMaterial
        fields = ['id', 'title', 'description', 'image', 'file', 'course']



