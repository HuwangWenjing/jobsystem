from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone

class token(models.Model):
    muser = models.OneToOneField('Manager', on_delete=models.CASCADE)
    tuser = models.OneToOneField('Teacher', on_delete=models.CASCADE)
    suser = models.OneToOneField('Student', on_delete=models.CASCADE)
    token = models.CharField(max_length=64, verbose_name='token')

class user(models.Model):
    '''用户登录表'''
    account = models.CharField(max_length=20, verbose_name='账号')
    name = models.CharField(max_length=20, verbose_name='姓名')
    identity = models.CharField(max_length=20, default='学生', verbose_name='身份')
    password = models.CharField(max_length=32, verbose_name='密码')

    class Meta:
        verbose_name = '用户登录表'
        verbose_name_plural = verbose_name
        unique_together = ('account', 'identity',)

class student(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    StuNo = models.CharField(max_length=50,verbose_name='学生学号',primary_key=True)
    StuName = models.CharField(max_length=50, verbose_name='学生姓名')
    StuSex = models.CharField(max_length=30, verbose_name='学生性别', choices=gender, default='女', null=True)
    Major = models.CharField(max_length=50, verbose_name='专业名称', null=True)
    StuPassWord = models.CharField(max_length=16, verbose_name='学生密码', default='123456')

    CuNo = models.ManyToManyField(
        'course',
        related_name='students',
        verbose_name='学生选修的课程编号'
    )

    need_to_sign = models.ManyToManyField(
        'sign',
        related_name='students',
        verbose_name='需要进行此次签到的学生'
    )


    def __str__(self):
        return self.StuName

    class Meta:
        ordering = ['-Major', 'StuNo']
        verbose_name = '学生'
        verbose_name_plural = '学生'

class manager(models.Model):
    MaNo = models.CharField(max_length=50,verbose_name='管理员编号',primary_key=True)
    MaName = models.CharField(max_length=50, verbose_name='管理员姓名')
    MaPassWord = models.CharField(max_length=16, verbose_name='管理员密码', default='123456')

class submission(models.Model):
    SubNo = models.CharField(max_length=50, verbose_name='提交编号',primary_key=True)
    Ans = models.CharField(max_length=50, verbose_name='学生答案', null=True, blank=True)
    Score = models.FloatField(verbose_name='作业成绩')
    SubTime = models.DateTimeField(verbose_name='提交时间',default=timezone.now)

    HomeNo = models.ForeignKey(
        'homework',
        on_delete=models.CASCADE,
        verbose_name='作业编号'
    )

    def __str__(self):
        return self.StuNo

    class Meta:
        ordering = ['-SubTime']

class notice(models.Model):
    NoticeNo = models.AutoField(primary_key=True)
    NoticeTitle = models.CharField(max_length=60, verbose_name='通知标题', default='通知标题')
    NoticeContent = models.CharField(max_length=5000, verbose_name='通知内容', default='通知内容')
    NoticePubTime = models.DateTimeField(verbose_name='通知发布时间', default=timezone.now)

    MaNo = models.ForeignKey(
        'manager',
        on_delete=models.CASCADE,
        verbose_name='发布此通知的管理员编号'
    )
    class Meta:
        verbose_name = '通知'
        verbose_name_plural = '通知'

class teacher(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    TeaNo = models.CharField(max_length=50,verbose_name='教师编号',primary_key=True)
    TeaName = models.CharField(max_length=50, verbose_name='教师姓名')
    TeaSex = models.CharField(max_length=30, verbose_name='教师性别', choices=gender, default='女', null=True)
    TeaPassWord = models.CharField(max_length=16, verbose_name='教师密码', default='888888')

    def __str__(self):
        return self.TeaName

    class Meta:
        ordering = ['-TeaName']
        verbose_name = '教师'
        verbose_name_plural = '教师'


class course(models.Model):
    CuNo = models.CharField(max_length=50, verbose_name='课程编号', primary_key=True)
    CuName = models.CharField(max_length=50, verbose_name='课程名称')

    TeaNo = models.OneToOneField(
        'teacher',
        on_delete=models.CASCADE,
        verbose_name='上这门课程的教师编号'
    )

    StuNo = models.ManyToManyField(
        'student',
        related_name='courses',
        verbose_name='选修这门课程的学生学号'
    )

    def __str__(self):
        return self.CuName

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = '课程'


#和question一对多
class homework(models.Model):
    HomNo = models.IntegerField(verbose_name='作业id', primary_key=True)
    Title = models.CharField(max_length=50, verbose_name='作业标题', default='a')
    PubDate = models.DateField(verbose_name='发布日期', default=timezone.now)

    CuNo = models.ForeignKey(
        'course',
        on_delete=models.CASCADE,
        verbose_name='课程编号'
    )

    class Meta:
        ordering = ['-PubDate']

    def __str__(self):
        return self.Title

class gradeanalysis(models.Model):
    AnaNo = models.IntegerField(verbose_name='分析id', primary_key=True)
    SubNums = models.FloatField(verbose_name='需要提交此次作业的人数')
    SubAvg = models.FloatField(verbose_name='平均成绩')
    SubMax = models.FloatField(verbose_name='最高成绩')
    SubMin = models.FloatField(verbose_name='最低成绩')
    SubDiff = models.FloatField(verbose_name='成绩差')
    excellentnums = models.FloatField(verbose_name='优秀人数')
    passnums = models.FloatField(verbose_name='及格人数')

    HomeNo = models.ForeignKey(
        'homework',
        on_delete=models.CASCADE,
        verbose_name='作业编号'
    )

    def __str__(self):
        return self.StuNo

    class Meta:
        ordering = ['AnaNo']#？？？？？？


class question(models.Model):
    QuesNo = models.IntegerField(verbose_name='题号', primary_key=True)
    Cont = models.CharField(max_length=5000, verbose_name='题目')
    CorAns = models.CharField(max_length=5000, verbose_name='题目答案')

    HomNo = models.ForeignKey(
        'homework',
        verbose_name='作业id',
        on_delete=models.CASCADE
    )


    class Meta:
        ordering = ['-QuesNo']

    def __str__(self):
        return self.Cont


class studentsign(models.Model):#(学生签到表）
    StuNo = models.CharField(max_length=50, verbose_name='学生学号')
    SubTime = models.DateTimeField(verbose_name='签到时间', default=timezone.now)
    CuNo = models.ForeignKey(
        'course',
        on_delete=models.CASCADE,
        verbose_name='课程编号'
    )



    def __str__(self):
        return self.StuNo

    class Meta:
        verbose_name = '学生签到'
        verbose_name_plural = '学生签到'

class sign(models.Model):#（教师发布签到表）
    SignNo = models.CharField(max_length=50, verbose_name='签到编号', primary_key=True)
    #StuNo = models.CharField(max_length=50, verbose_name='学生学号')
    SubTime = models.DateTimeField(verbose_name='签到时间', default=timezone.now)
    Deadline = models.DateTimeField(verbose_name='截止时间')
    CuNo = models.ForeignKey(
        'course',
        on_delete=models.CASCADE,
        verbose_name='课程编号'
    )
    sign_by = models.ManyToManyField(
        'student',
        related_name='students',
        verbose_name='需要进行此签到的学生'
    )

    def __str__(self):
        return self.StuNo

    class Meta:
        verbose_name = '签到'
        verbose_name_plural = '签到'


class viewsign(models.Model):#(学生签到表）
    #SignNo = models.CharField(max_length=50, verbose_name='签到编号', primary_key=True)
    VSNo= models.CharField(max_length=50, verbose_name='签到信息编号', primary_key=True)
    StuNo = models.CharField(max_length=50, verbose_name='学生学号')
    PubTime = models.DateTimeField(verbose_name='发布时间')
    Deadline = models.DateTimeField(verbose_name='截止时间')#1
    need_sign_by_nums = models.IntegerField(verbose_name="需要签到人数", null=True)
    sign_by_nums = models.IntegerField(verbose_name="已签到人数",null=True)
    not_sign_by_nums = models.IntegerField(verbose_name="未签到人数", null=True)

    CuNo = models.ForeignKey(
        'course',
        on_delete=models.CASCADE,
        verbose_name='课程编号'
    )


    def __str__(self):
        return self.StuNo

    class Meta:
        verbose_name = '签到信息'
        verbose_name_plural = '签到信息'