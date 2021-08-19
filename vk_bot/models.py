from django.db import models
from .static_data import GROUPS
from vk_bot.utils import sum_dict_values


class VKUser(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)

    COURSE_CHOICES = (
        (1, '1 курс'),
        (2, '2 курс'),
        (3, '3 курс'),
        (4, '4 курс'),
    )

    course = models.IntegerField(
        choices=COURSE_CHOICES,
        null=True,
        blank=True,
    )

    GROUP_CHOICES = tuple(
        zip(sum_dict_values(GROUPS), sum_dict_values(GROUPS))
    )

    group = models.CharField(
        max_length=8,
        choices=GROUP_CHOICES,
        null=True,
        blank=True,
    )

    REG_COURSE = 'reg1'
    REG_GROUP = 'reg2'
    ANY = 'any'
    LINK = 'link'
    SCHEDULE = 'sch'

    USER_STATUS = (
        (REG_COURSE, 'Course registration'),
        (REG_GROUP, 'Group registration'),
        (ANY, 'Available for any function'),
        (LINK, 'Links to classes'),
        (SCHEDULE, 'Schedule')
    )

    status = models.CharField(
        max_length=4,
        choices=USER_STATUS,
        default='any',
    )

    date = models.DateField()

    class Meta:
        ordering = ["name", "surname"]

    def __str__(self):
        return "{0} {1}".format(self.name, self.surname)

    @classmethod
    def get_user(cls, user_id):
        if cls.objects.filter(id__exact=user_id):
            return cls.objects.get(id=user_id)

    @classmethod
    def update(cls, user_id, **kwargs):
        cls.objects.filter(
            id__exact=user_id).update(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        cls.objects.create(**kwargs)

    @classmethod
    def create_or_pass(cls, **kwargs):
        user_id = kwargs.get('id')
        if not cls.objects.filter(id__exact=user_id):
            cls.create(**kwargs)


class VKMessage(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(
        VKUser,
        on_delete=models.SET_NULL,
        null=True
    )
    text = models.CharField(max_length=4096)
    date = models.DateField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return "{0}".format(self.id)

    @classmethod
    def create(cls, **kwargs):
        cls.objects.create(**kwargs)

