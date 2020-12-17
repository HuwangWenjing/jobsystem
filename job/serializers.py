from rest_framework import serializers
from .models import manager, teacher, student, sign, notice, course, homework, gradeanalysis, studentsign, viewsign


class MaInfoSer(serializers.ModelSerializer):

    class Meta:
        model = manager
        fields = '__all__'


class TeaInfoSer(serializers.ModelSerializer):

    class Meta:
        model = teacher
        fields = '__all__'


class StuInfoSer(serializers.ModelSerializer):

    class Meta:
        model = student
        fields = '__all__'


class HomSer(serializers.ModelSerializer):

    class Meta:
        model = homework
        fields = '__all__'


class SignSer(serializers.ModelSerializer):
    students = serializers.StringRelatedField(many=True)

    class Meta:
        model = sign
        fields = '__all__'


class CouSer(serializers.ModelSerializer):

    class Meta:
        model = course
        fields = '__all__'

class GraAnaSer(serializers.ModelSerializer):

    class Meta:
        model = gradeanalysis
        fields = '__all__'

class StudentSignSer(serializers.ModelSerializer):

    class Meta:
        model = studentsign
        fields = '__all__'

class ViewSignSer(serializers.ModelSerializer):

    class Meta:
        model = viewsign
        fields = '__all__'
class NoticeSer(serializers.ModelSerializer):

    class Meta:
        model = notice
        fields = '__all__'
