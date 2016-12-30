from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


# Create your models here.

class IDC(models.Model):
    """机房"""
    name = models.CharField(max_length=64, unique=True, verbose_name='机房名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'IDC机房'
        verbose_name_plural = 'IDC机房'


class Host(models.Model):
    """主机
    hostname:主机名(唯一
    ip_addr:ip地址
    port:端口(默认22
    idc:外键
    system_type:系统
    memo:备注
    enabled:是否启用
    """
    hostname = models.CharField(max_length=64, unique=True, verbose_name='主机名')
    id_addr = models.GenericIPAddressField(verbose_name='IP地址')
    port = models.SmallIntegerField(default=22, verbose_name='端口')
    idc = models.ForeignKey('IDC', blank=True, null=True, verbose_name='IDC机房')
    system_type_choices = ((0, 'Linux'), (1, 'Windows'))
    system_type = models.SmallIntegerField(choices=system_type_choices, default=0, verbose_name='操作系统')
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name='备注')
    enabled = models.BooleanField(default=True, verbose_name='启用本机')

    class Meta:
        """联合唯一"""
        unique_together = ('id_addr', 'port')
        verbose_name = '主机'
        verbose_name_plural = '主机'

    def __str__(self):
        return "%s(%s)" % (self.hostname, self.id_addr)


class RemoteUser(models.Model):
    """存储远程用户信息
    auth_type:连接方式
    username:用户名
    password:密码
    """
    auth_type_choices = ((0, 'ssh-password'), (1, 'ssh-key'))
    auth_type = models.SmallIntegerField(choices=auth_type_choices, default=0, verbose_name='连接方式')
    username = models.CharField(max_length=128, verbose_name='账号')
    password = models.CharField(max_length=256, help_text='如果auth_type选择为ssh-key,那么此处就应该是key', verbose_name='密码')

    class Meta:
        unique_together = ('auth_type', 'username', 'password')
        verbose_name = '远程用户'
        verbose_name_plural = '远程用户'

    def __str__(self):
        return self.username


class BindHost(models.Model):
    """关联远程主机与远程用户"""
    host = models.ForeignKey('Host')
    remote_user = models.ForeignKey('RemoteUser')

    class Meta:
        unique_together = ('host', 'remote_user')
        verbose_name = '主机关联用户'
        verbose_name_plural = '主机关联用户'

    def __str__(self):
        return "<%s:%s>" % (self.host.hostname, self.remote_user.username)


class HostGroups(models.Model):
    """用户组"""
    name = models.CharField(max_length=64, unique=True)
    bind_hosts = models.ManyToManyField('BindHost', blank=True)
    memo = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '主机组'
        verbose_name_plural = '主机组'


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
                email=self.normalize_email(email),
                name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
                email,
                password=password,
                name=name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    """堡垒机账户"""
    email = models.EmailField(
            verbose_name='email address',
            max_length=255,
            unique=True,
    )
    name = models.CharField(max_length=256)
    bind_hosts = models.ManyToManyField('BindHost', blank=True, null=True)
    host_groups = models.ManyToManyField('HostGroups', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = '堡垒机账户'
        verbose_name_plural = '堡垒机账户'