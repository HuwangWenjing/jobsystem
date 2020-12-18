from django.contrib.auth.hashers import make_password
from django.db.models import Q, Count, Max, Min
from django.utils.datetime_safe import datetime

from job.models import *
from job.serializers import StuInfoSer, TeaInfoSer, NoticeSer, SignSer, GraAnaSer, StudentSignSer, ViewSignSer

import hashlib
from job.models import teacher, manager, student, course, question, token, homework
from job.serializers import MaInfoSer, TeaInfoSer, StuInfoSer, CouSer, HomSer
from rest_framework.views import APIView, Response
import time
from django.utils import timezone
#from django.contrib.auth.hashers import APIView,Response
from django.db.models import Avg, Sum

def md5(user):
    """md5 加密token"""
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()

def t_chk_token(token):
    if token is None:
        return Response({
            'info': '用户未登录',
            'code': 403
        }, status=403)
    t = token.objects.filter(token=token)
    if len(t) <= 0:
        # token无效
        return Response({
            'info': '无效用户',
            'code': 403
        }, status=403)
    return t.get().tuser.ok
def chk_sign_id(sign_id):
    try:
        S = sign.objects.get(sign_id)
    except:
        return Response({
            'info': '该签到不存在',
            'code': 403,
        }, status=403)
    return
def chk_homework_id(homework_id):
    try:
        h = homework.objects.get(pk=homework_id)
    except:
        return Response({
            'info': '该作业不存在',
            'code': 403,
        }, status=403)
    return h

def chk_course_id(cou_id):
    try:
        c = course.objects.get(pk=cou_id)
    except:
        return Response({
            'info': '该课程不存在',
            'code': 403,
        }, status=403)
    return c

def s_chk_token(token):
    if token is None:
        return Response({
            'info': '用户未登录',
            'code': 403
        }, status=403)
    t = token.objects.filter(token=token)
    if len(t) <= 0:
        # token无效
        return Response({
            'info': '无效用户',
            'code': 403
        }, status=403)
    return t.get().suser.ok

def m_chk_token(token):
    if token is None:
        return Response({
            'info': '用户未登录',
            'code': 403
        }, status=403)
    t = token.objects.filter(token=token)
    if len(t) <= 0:
        # token无效
        return Response({
            'info': '无效用户',
            'code': 403
        }, status=403)
    return t.get().muser.ok

def chk_notice_id(notice_id):
    try:
        n = notice.objects.get(pk=notice_id)
    except:
        return Response({
            'info': '该通知不存在',
            'code': 403,
        }, status=403)
    return n

class add_student(APIView):
    def post(self,request):
        token = request.META.get('token')
        student_id = request.POST.get('student_id')
        student_name = request.POST.get('student_name')
        student_sex = request.POST.get('student_sex')
        #student_password = request.POST.get('student_password')
        major = request.POST.get('major')
        if not all ([student_id,student_name,student_sex,major]):
            return Response({
                'info': '参数不完整',
                'code': 400,
            }, status=400)
            #print(token)
        manager_id = m_chk_token(token)
        if isinstance(manager_id, Response):
            return manager_id

        S=student.objects.get(StuNo=student_id)
        if len(S) > 0:
            return Response({
                'info': '该同学已存在',
                'code': 403
            }, status=403)

        S = student.objects.create(
            StuNo = student_id,
            StuName = student_name ,
            StuSex = student_sex ,
            Major = major
        )
        return Response({
            'info': 'success',
            'code': 200,
            'data': StuInfoSer(S).data
        }, status=200)

class add_teacher(APIView):
    def post(self, request):
        token = request.META.get('token')
        teacher_id = request.POST.get('teacher_id')
        teacher_name = request.POST.get('teacher_name')
        teacher_sex = request.POST.get('teacher_sex')
        major = request.POST.get('major')
        if not all ([teacher_id,teacher_name,teacher_sex,major]):
            return Response({
                'info': '参数不完整',
                'code': 400,
            }, status=400)

        manager_id = m_chk_token(token)
        if isinstance(manager_id, Response):
            return manager_id

        Tea = teacher.objects.get(TeaNo=teacher_id)
        if len(Tea) > 0:
            return Response({
                'info': '该教师已存在',
                'code': 403
            }, status=403)

        T=teacher.objects.create(
            TeaNo=teacher_id,
            TeaName=teacher_name,
            TeaSex=teacher_sex,
            Major=major,
            )
        return Response({
                'info': 'success',
                'code': 200,
                'data': TeaInfoSer(T).data
            }, status=200)

class add_course(APIView):
    def post(self, request):
        token = request.META.get('token')
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course_name')
        teacher_id = request.POST.get('teacher_id')
        student_id = request.POST.get('student_id')
        if not all ([course_id,course_name,teacher_id]):
            return Response({
                'info': '参数不完整',
                'code': 400,
            }, status=400)
        manager_id = m_chk_token(token)
        if isinstance(manager_id, Response):
            return manager_id

        Co = course.objects.get(pk=course_id)
        if len(Co) > 0:
            return Response({
                'info': '该课程已存在',
                'code': 403
            }, status=403)

        C = course.objects.create(
            CuNo=course_id,
            CuName=course_name,
            TeaNo=teacher_id,
            StuNo=student_id,
        )
        return Response({
            'info': 'success',
            'code': 200,
            'data': CouSer(C).data
        }, status=200)

class publish_notice(APIView):
    def post(self,request):
        token = request.META.get('HTTP_TOKEN')
        notice_id = request.POST.get('notice_id')
        notice_title = request.POST.get("notice_title")
        notice_comment = request.POST.get('notice_comment')
        if not all ([notice_id,notice_title,notice_comment]):
            return Response({
                'info': '参数不完整',
                'code': 400,
            }, status=400)
        manager_id = m_chk_token(token)
        if isinstance(manager_id, Response):
            return manager_id

        No = notice.objects.get(pk=notice_id)
        if len(No) > 0:
            return Response({
                'info': '该通知已存在',
                'code': 403
            }, status=403)

        N=notice.objects.create(
            NoticeId=notice_id,
            NoticeTitle=notice_title,
            NoticeContent=notice_comment
        )

        return Response({
            'info': 'success',
            'code': 200,
            'data': NoticeSer(N).data
        }, status=200)

class modify_student(APIView):
    def post(self,request):
        token = request.META.get('token')
        student_id = request.POST.get('student_id')
        if student_id is None:
            return Response({
                'info': '参数不完整',
                'code': 400,
            }, status=400)
        manager_id = m_chk_token(token)
        if isinstance(manager_id, Response):
            return manager_id

        student_id = s_chk_token(token)
        if isinstance(student_id, Response):
            return student_id
        S = student.objects.get(pk=student_id)

        student_name = request.POST.get('student_name')
        student_sex = request.POST.get('student_sex')
        student_password = request.POST.get('student_password')
        major = request.POST.get('major')

        S.StuName=student_name
        S.StuSex=student_sex
        S.StuPassword=student_password
        S.Major=major

        S.save()

        return Response({
            'info': 'success',
            'code': 200,
            'data': StuInfoSer(S).data
        }, status=200)

class modify_teacher(APIView):
    def post(self,request):
        token = request.META.get('token')
        teacher_id = request.POST.get('teacher_id')
        if teacher_id is None:
            return Response({
                'info': '参数不完整',
                'code': 400,
            }, status=400)

        manager_id = m_chk_token(token)
        if isinstance(manager_id, Response):
            return manager_id


        teacher_id = t_chk_token(token)
        if isinstance(teacher_id, Response):
            return teacher_id
        T = teacher.objects.get(pk=teacher_id)

        teacher_name = request.POST.get('teacher_name')
        teacher_sex = request.POST.get('teacher_sex')
        teacher_password = request.POST.get('teacher_password')
        major = request.POST.get('major')

        T.TeaName=teacher_name
        T.TeaSex=teacher_sex
        T.TeaPassword=teacher_password
        T.Major=major

        T.save()

        return Response({
            'info': 'success',
            'code': 200,
            'data': TeaInfoSer(T).data
        }, status=200)

class modify_course(APIView):
    def post(self, request):
        token = request.META.get('token')
        course_id = request.POST.get('course_id')
        if course_id is None:
            return Response({
                'info': '参数不完整',
                'code': 400,
            }, status=400)

        manager_id = m_chk_token(token)
        if isinstance(manager_id, Response):
            return manager_id


        course_id = chk_course_id(course_id)
        if isinstance(course_id, Response):
            return course_id
        C = course.objects.get(pk=course_id)

        course_name = request.POST.get('course_name')
        teacher_id = request.POST.get('teacher_id')
        student_id = request.POST.get('student_id')


        C.CuName = course_name
        C.TeaNo = teacher_id
        C.StuNo = student_id

        C.save()

        return Response({
            'info': 'success',
            'code': 200,
            'data': CouSer(C).data
        }, status=200)

class delete_student(APIView):
    def post(self,request):
        token = request.META.get('token')
        student_id = request.POST.get('student_id')
        if student_id is None:
            return Response({
                'info': '参数不完整',
                'code': 400,
            }, status=400)

        manager_id = m_chk_token(token)
        if isinstance(manager_id, Response):
            return manager_id

        student_id = s_chk_token(token)
        if isinstance(student_id, Response):
            return student_id
        S = student.objects.get(pk=student_id)
        course.objects.filter(StuNo=student_id).delete()
        studentsign.objects.filter(StuNo=student_id).delete()

        S.delete()

        return Response({
            'info': 'success',
            'code': 200,
            'data': StuInfoSer(S).data
        }, status=200)

class delete_teacher(APIView):
    def post(self,request):
        token = request.META.get('token')
        teacher_id = request.POST.get('teacher_id')
        if teacher_id is None:
            return Response({
                'info': '参数不完整',
                'code': 400,
            }, status=400)

        manager_id = m_chk_token(token)
        if isinstance(manager_id, Response):
            return manager_id


        teacher_id = t_chk_token(token)
        if isinstance(teacher_id, Response):
            return teacher_id
        T = teacher.objects.get(pk=teacher_id)
        course.objects.filter(TeaNo=teacher_id).delete()
        sign.objects.get(CuNo=T.CuNo).delete()

        T.delete()

        return Response({
            'info': 'success',
            'code': 200,
            'data': TeaInfoSer(T).data
        }, status=200)

class delete_course(APIView):
    def post(self, request):
        token = request.META.get('token')
        course_id = request.POST.get('course_id')
        if course_id is None:
            return Response({
                'info': '参数不完整',
                'code': 400,
            }, status=400)

        manager_id = m_chk_token(token)
        if isinstance(manager_id, Response):
            return manager_id


        course_id = chk_course_id(course_id)
        if isinstance(course_id, Response):
            return course_id
        C = course.objects.get(pk=course_id)
        homework.objects.filter(CuNo=course_id).delete()
        sign.objects.filter(CuNo=course_id).delete()

        C.delete()

        return Response({
            'info': 'success',
            'code': 200,
            'data': CouSer(C).data
        }, status=200)

class delete_notice(APIView):
    def post(self,request):
        token = request.META.get('HTTP_TOKEN')
        notice_id = request.POST.get('notice_id')
        if notice_id is None :
            return Response({
                'info': '参数不完整',
                'code': 400,
            }, status=400)
        manager_id = m_chk_token(token)
        if isinstance(manager_id, Response):
            return manager_id

        notice_id = chk_notice_id(notice_id)
        if isinstance(notice_id, Response):
            return notice_id

        N = notice.objects.filter(pk=notice_id)
        N.delete()

        return Response({
            'info': 'success',
            'code': 200,
            'data': NoticeSer(N).data
        }, status=200)


class delete_homework(APIView):
    def post(self, request):
        token = request.META.get('token')
        homework_id = request.POST.get('homework_id')
        if homework_id is None:
            return Response({
                'info': '参数不完整',
                'code': 400,
            }, status=400)

        teacher_id = t_chk_token(token)
        if isinstance(teacher_id, Response):
            return teacher_id


        homework_id = chk_homework_id(homework_id)
        if isinstance(homework_id, Response):
            return homework_id
        H = homework.objects.get(pk=homework_id)
        S = submission.objects.filter(HomeNo=homework_id)

        if len(S) > 0:
            S.delete()

        H.dalete()
        return Response({
            'info': 'success',
            'code': 200,
            'data': HomSer(H).data
        }, status=200)

class delete_sign(APIView):
    def post(self, request):
        token = request.META.get('token')
        course_id = request.POST.get('course_id')
        if course_id is None:
            return Response({
                'info': '参数不完整',
                'code': 400,
            }, status=400)

        teacher_id = t_chk_token(token)
        if isinstance(teacher_id, Response):
            return teacher_id


        course_id = chk_course_id(course_id)
        if isinstance(course_id, Response):
            return course_id
        Ss = studentsign.objects.filter(CuNo=course_id)
        if  len(Ss) > 0 :
            Ss.dalete()

        S = sign.objects.filter(CuNo=course_id)
        S.dalete()

        return Response({
            'info': 'success',
            'code': 200,
            'data': SignSer(S).data
        }, status=200)



class publishsign(APIView):#（教师发布签到）
    def post(self,request):
        token = request.META.get('token')
        course_id = request.POST.get('course_id')
        SignNo = request.POST.get("sign_id")
        PubTime = request.POST.get("Pubtime")
        Deadline = request.POST.get("deadline")

        if not all ([course_id,SignNo,PubTime,Deadline]):
            return Response({
                'info': '参数不完整',
                'code': 400,
            }, status=400)

        teacher_id = t_chk_token(token)
        if isinstance(teacher_id, Response):
            return teacher_id

        course_id = chk_course_id(course_id)
        if isinstance(course_id, Response):
            return course_id
        C = course.objects.filter(CuNo=course_id)
        S = C.StuNo

        S=sign.objects.create(
            SignNo=SignNo,
            sign_by = S ,
            PubTime = PubTime,
            Deadline = Deadline,
            CuNo = course_id
        )

        return Response({
            'info': 'success',
            'code': 200,
            'data': SignSer(S).data
        }, status=200)

class Sign(APIView):#（学生签到）
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        course_id = request.GET.get('course_id')

        if course_id is None:
            return Response({
                'info': '参数不完整',
                'code': 400,
            }, status=400)

        student_id = s_chk_token(token)
        if isinstance(student_id, Response):
            return student_id


        C = chk_course_id(course_id)
        if isinstance(C, Response):
            return C

        if studentsign.objects.filter(StuNo=student_id, CuNo=course_id):
            return Response({
                'info': '你已经签过到了',
                'code': 403,
            }, status=403)

        time_now = timezone.now()
        expired_sign = sign.objects.filter(student=student_id, course=course_id, Deadline_lte=time_now)

        if len(expired_sign) > 0:
            return Response({
                'info': '签到已过期',
                'code': 403,
            }, status=403)


        Ss=studentsign.objects.create(
            StuNo=student_id,
            SubTime = time_now,
            CuNo = course_id
        )
        return Response({
            'info': 'success',
            'code': 200,
            'data': StudentSignSer(Ss).data
        }, status=200)##



        return Response({
            'info': 'success',
            'code': 200,
            'data': ViewSignSer(VS).data
        }, status=200)
    
class teacher_get_sign(APIView):
    def get(self, request):
        token=request.META.get('token')
        course_id=request.GET.get('course_id')

        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id

        c = chk_course_id(course_id)
        if isinstance(c, Response):
            return c
        C = course.objects.get(pk=course_id)

        Sign = studentsign.objects.filter(CuNo=course_id)
        sign.need_sign_by_nums=C.aggregate(Count('StuNo'))
        Sign.sign_by_nums = Sign.aggregate(Count('StuNo'))#Sign.StuNo.count()
        Sign.save()

        return Response({
            'info': 'success',
            'code': 200,
            'data': StudentSignSer(Sign).data
        }, status=200)

class teacher_get_sign_detail(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        course_id = request.GET.get('course_id')

        tea_id = t_chk_token(token)
        if isinstance(tea_id, Response):
            return tea_id

        c = chk_course_id(course_id)
        if isinstance(c, Response):
            return c

        Studentsign = studentsign.objects.filter(course_id__pk=course_id)

        return Response({
            'info': 'success',
            'code': 200,
            'data': StudentSignSer(Studentsign).data
        }, status=200)

class stuchangepasswork(APIView):

    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        student_id = request.POST.get('student_id')
        student_name = request.POST.get('student_name')
        pass_new = request.POST.get('new_password')

        student_id = s_chk_token(token)
        if isinstance(student_id, Response):
            return student_id

        if not all([student_id,student_name, pass_new]):
            return Response({
                'info': '参数不完整',
                'code': 400
            }, status=400)
        S = student.objects.get(pk=student_id)
        if S.StuPassword == pass_new:
            return Response({
                'info': '新密码与旧密码重复',
                'code': 403
            }, status=403)
        S.StuPassWord = make_password(pass_new)
        S.save()
        return Response({
            'info': 'success',
            'code': 200,
            'data': StuInfoSer(S).data
        }, status=200)
    
class student_get_sign(APIView):
    def get(self, request):
        token = request.META.get('HTTP_TOKEN')
        course_id = request.GET.get('course_id')

        stu_id = s_chk_token(token)
        if isinstance(stu_id, Response):
            return stu_id

        c = chk_course_id(course_id)
        if isinstance(c, Response):
            return c
        time_now = timezone.now()
        expired_sign = sign.objects.filter(course=course_id, Deadline_lte=time_now)
        if len(expired_sign) > 0:
            return Response({
                'info': '签到已过期',
                'code': 403,
            }, status=403)

        Sign = sign.objects.filter(course_id=course_id)

        return Response({
            'info': 'success',
            'code': 200,
            'data': SignSer(Sign).data
        }, status=200)
    
class teachangepasswork(APIView):

    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        teacher_id = request.POST.get('teacher_id')
        teacher_name = request.POST.get('teacher_name')
        pass_new = request.POST.get('new_password')

        teacher_id = t_chk_token(token)
        if isinstance(teacher_id, Response):
            return teacher_id

        if not all([teacher_id,teacher_name, pass_new]):
            return Response({
                'info': '参数不完整',
                'code': 400
            }, status=400)
        T = teacher.objects.get(pk=teacher_id)
        if T.TeaPassword == pass_new :
            return Response({
                'info': '新密码与旧密码重复',
                'code': 403
            }, status=403)

        T.TeaPassWord = make_password(pass_new)
        T.save()
        return Response({
            'info': 'success',
            'code': 200,
            'data': TeaInfoSer(T).data
        }, status=200)

class machangepasswork(APIView):
    def post(self, request):
        token = request.META.get('HTTP_TOKEN')
        manager_id = request.POST.get('manager_id')
        manager_name = request.POST.get('manager_name')
        pass_new = request.POST.get('new_password')

        manager_id = m_chk_token(token)
        if isinstance(manager_id, Response):
            return manager_id

        if not all([manager_id, manager_name, pass_new]):
            return Response({
                'info': '参数不完整',
                'code': 400
            }, status=400)
        M = manager.objects.get(pk=manager_id)
        if M.MaPassword == pass_new:
            return Response({
                'info': '新密码与旧密码重复',
                'code': 403
            }, status=403)

        M.MaPassWord = make_password(pass_new)
        M.save()
        return Response({
            'info': 'success',
            'code': 200,
            'data': MaInfoSer(M).data
        }, status=200)
