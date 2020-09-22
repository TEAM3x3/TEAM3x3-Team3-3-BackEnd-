from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Gender_Choice(models.TextChoices):
        MALE = 'M', ('Male')
        FEMALE = 'F', ('Female')
        NONETYPE = 'N', ('None')

    nickname = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField('핸드폰 번호', max_length=15)
    gender = models.CharField('성별', max_length=1, choices=Gender_Choice.choices, default=Gender_Choice.NONETYPE)
    birthday = models.DateField(max_length=11, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='가입일')

    def save(self, *args, **kwargs):
        from carts.models import Cart
        if self.id is None:
            super().save(*args, **kwargs)
            Cart.objects.create(user=self)
        else:
            super().save(*args, **kwargs)
    # REQUIRED_FIELDS = ['email']


class UserAddress(models.Model):
    class Location_Choice(models.TextChoices):
        FRONT_DOOR = 'fd', ('문 앞')
        SEQURITY_OFFICE = 'so', ('경비실')
        DELIVERY_BOX = 'db', ('우편함')
        ETC = 'etc', ('기타')

    address = models.CharField(max_length=200)
    detail_address = models.CharField(max_length=200)
    require_message = models.CharField('요청 사항', max_length=100)
    status = models.CharField('기본 배송지', max_length=1, default=False)
    recieving_place = models.CharField('받으실 장소', max_length=3,
                                       choices=Location_Choice.choices,
                                       default=Location_Choice.ETC,
                                       null=True)
    entrance_password = models.CharField('공동현관 비밀번호', max_length=10, null=True)
    free_pass = models.BooleanField('공동현관 자유출입 가능 여부', default=False)
    etc = models.CharField('기타', max_length=100, null=True)
    message = models.BooleanField('배송완료 메시지 전송 여부', default=False, null=True)

    user = models.ForeignKey(
        'members.User',
        on_delete=models.CASCADE,
        related_name='address',
    )


class UserSearch(models.Model):
    user = models.ForeignKey('members.User', on_delete=models.CASCADE, related_name='search')
    keyword = models.ForeignKey('members.Keyword', on_delete=models.CASCADE, related_name='search')
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'keyword')

    def save(self, *args, **kwargs):
        count_word = self.keyword
        if count_word:
            self.keyword.count += 1
            self.keyword.save()
            super().save(*args, **kwargs)


class KeyWord(models.Model):
    name = models.CharField(max_length=100, unique=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

# class Profile(models.Model):

#     COUPON_CHOICES = (
#         ('A', '[신규가입쿠폰] 10% 할인'),
#         ('B', '[농할갑시다] 햇농산물 20%'),
#     )
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     grade = models.OneToOneField(User, on_delete=models.CASCADE)
#     coupon = models.CharField('쿠폰', max_length=1, choices=COUPON_CHOICES)
#     accumulated_money = models.IntegerField('적립금', default=0)
#     point = models.IntegerField('포인트', default=0)
