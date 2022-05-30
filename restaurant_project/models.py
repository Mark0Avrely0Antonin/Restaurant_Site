from django.conf import settings

from django.urls import reverse
from django.contrib.auth.models import *

from django.contrib.auth.models import PermissionsMixin


# Create your models here.

class Manager_Account(BaseUserManager):

    def create_user(self, email, username, password = None, **other_fields):

        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email = email, username = username, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_email_verified', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        email = self.normalize_email(email)
        user = self.model(email = email, username = username, **other_fields)
        user.set_password(password)
        user.profile_username = username
        user.save()
        return user


class User_Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name = 'Почта пользователя', unique = True)
    username = models.CharField(max_length = 150, unique = True, verbose_name = 'Имя пользователя')

    time_create = models.DateTimeField(auto_now_add = True, verbose_name = 'Зарегистрирован')
    time_update = models.DateTimeField(auto_now = True, verbose_name = 'Был последний раз')

    profile_username = models.SlugField(verbose_name = 'Профильное имя', max_length = 50, blank = True)

    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_email_verified = models.BooleanField(default = False)

    objects = Manager_Account()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f' {self.username} - {self.email}'




    class Meta:
        verbose_name = 'Аккаунт пользователя'
        verbose_name_plural = 'Аккаунты пользователей'


class Profile(models.Model):
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE,
                                   verbose_name = 'Аккаунт профиля')
    bio = models.TextField(verbose_name = 'Биография пользователя', blank = True)
    country = models.CharField(verbose_name = 'Страна пользователя', max_length = 25, blank = True)
    account_image = models.ImageField(upload_to = 'media/%Y/%m/%d', verbose_name = 'Изображения пользователя',
                                      blank = True)

    profile_username = models.SlugField(verbose_name = 'Профильное имя', max_length = 50, null = True)

    def __str__(self):
        return str(self.account)

    def get_absolute_url(self):
        return reverse("profile_view", kwargs = {"slug": self.profile_username})




    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Category(models.Model):
    name = models.CharField(max_length = 255, verbose_name = "Названия категорий")
    url = models.URLField(verbose_name = 'Иконка категорий', null = True)

    def __str__(self):
        return self.name




    class Meta:
        verbose_name = 'Категория блюда'
        verbose_name_plural = 'Категорий блюда'


class Menu(models.Model):
    name = models.CharField(max_length = 255, verbose_name = 'Название блюдо')
    content = models.TextField(verbose_name = 'О блюдо')
    price = models.IntegerField(verbose_name = 'Цена блюдо')
    photo = models.URLField(verbose_name = 'Фотография блюдо', null = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, verbose_name = 'Категорий блюдо', null = True)
    url = models.SlugField(max_length = 25, null = True)

    dish_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name = 'Лайки блюдо',
                                        related_name = 'dish_likes')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("view_dish", kwargs = {"slug": self.url})

    def dish_total_likes(self):
        return self.dish_likes.count()

    def get_review(self):
        return self.reviews_set.filter().order_by('-review_likes')




    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'


class Reviews(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE,
                             verbose_name = 'Пользователь комментария')
    content = models.TextField(verbose_name = 'Контент пользователя')
    dish = models.ForeignKey(Menu, on_delete = models.CASCADE, verbose_name = 'Блюдо пользователя')
    created_at = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата комментария')
    parent = models.ForeignKey('self', verbose_name = 'Родитель', on_delete = models.SET_NULL, blank = True,
                               null = True)

    review_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'review_likes',
                                          verbose_name = 'Review Likes')
    review_unlikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'review_unlikes',
                                            verbose_name = 'Review unlikes')

    def __str__(self):
        return f'{str(self.user)} - {str(self.dish)}'

    def review_total_likes(self):
        return self.review_likes.count()

    def review_total_unlikes(self):
        return self.review_unlikes.count()




    class Meta:
        verbose_name = 'Комментарий о блюда'
        verbose_name_plural = 'Комментарий о блюда'


class ContactReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = 'Пользователь комментария',
                             on_delete = models.CASCADE)
    comment = models.TextField(verbose_name = 'Комментарий')
    time_created = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата комментария')

    def __str__(self):
        return f'{str(self.user)} - {str(self.time_created)}'




    class Meta:
        verbose_name = 'Комментарий контакту'
