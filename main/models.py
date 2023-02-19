from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.dispatch import receiver
from django.db.models.signals import pre_save

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Test(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    maximum_attemps = models.PositiveBigIntegerField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=(timezone.now()+timezone.timedelta(days=5)))
    pass_persontags = models.PositiveBigIntegerField()

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.CharField(max_length=300)
    a = models.CharField(max_length=150)
    b = models.CharField(max_length=150)
    c = models.CharField(max_length=150)
    d = models.CharField(max_length=150)
    tru_answer = models.CharField(max_length=150, help_text="E.x a")

    def __str__(self):
        return self.question



class CheckTest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    finded_question = models.PositiveBigIntegerField(default=0)
    user_passed = models.BooleanField(default=False)
    percentage = models.PositiveBigIntegerField(default=0)

    def __str__(self) -> str:
        return "Test off" + str(self.student.username)



class CheckQuestion(models.Model):
    checktest = models.ForeignKey(CheckTest, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    given_answer = models.CharField(max_length=1, help_text="E.x: a")
    tru_answer = models.CharField(max_length=1, help_text="E.x: a")
    is_true = models.BooleanField(default=False)


@receiver(pre_save, sender=CheckQuestion)
def check_answer(sender, instance, *args, **kwargs):
    if instance.given_answer == instance.tru_answer:
        instance.is_true=True



@receiver(pre_save, sender=CheckTest)
def check_test(sender, instance, *args, **kwargs):
    checktest = instance
    checktest.finded_question = CheckQuestion.objects.filter(checktest=checktest, is_true=True).count()
    try:
        checktest.percentage = int(checktest.finded_question)*100//CheckQuestion.objects.filter(checktest=checktest).count()
        if checktest.test.pass_persontags <= checktest.percentage:
            checktest.user_passed=True
    except:pass