from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.utils import timezone
from common.utility import get_ulid

class UserManager(UserManager):
    '''
    カスタムUserモデルを作成したため、UserManagerもオーバーライドする
    '''    
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
    
    
class User(AbstractBaseUser, PermissionsMixin):
    """　
    カスタムUserモデル
    """
    id = models.CharField(max_length=32, default=get_ulid,
                            primary_key=True, editable=False)
    username_validator = UnicodeUsernameValidator()
    full_name = models.CharField(_('氏名'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True, unique=True, db_index=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # Custom
    mercari_user_id = models.CharField(_('メルカリユーザーID'), max_length=32, blank=True)
    mercari_user_name = models.CharField(_('メルカリユーザー名'), max_length=64, blank=True)
    agent_password = models.CharField(_('Agentパスワード'), max_length=32, blank=True, null=True)
    agent_password_expire_at = models.DateTimeField(_('Agentパスワード期限'), blank=True, null=True)
    picture = models.CharField(_('プロフィールアイコン'), max_length=256, blank=True, null=True)
    email_verified = models.BooleanField(_('Email確認済'), blank=True, null=True)
    plan_id = models.IntegerField(_('契約プラン'), blank=True, null=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', ]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = "auth_user"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    # 既存メソッドの変更
    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name
    

