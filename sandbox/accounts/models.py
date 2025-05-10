from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    """"ユーザー管理クラス"""
    
    def create_user(self, email, name, password=None):
        """ユーザー作成

        Args:
            email (str): メールアドレス
            name (str): ユーザー名
            password (str, optional): パスワード、デフォルトでNone

        Raises:
            ValueError: メールアドレスがブランク

        Returns:
            user: Userインスタンス
        """
        if not email:
            raise ValueError('メールアドレスは必須です')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):#管理ユーザーのフィールドを作成
        """管理者ユーザー作成

        Args:
            email (str): 管理者メールアドレス
            name (str): 管理者ユーザー名
            password (str, optional): パスワード、デフォルトでNone

        Returns:
            user: Userインスタンス
        """
        user = self.create_user(
            email=email,
            name=name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """Userテーブル定義"""
    
    #メールアドレス
    email = models.EmailField(
        verbose_name='メールアドレス',
        max_length=255,
        unique=True,
    )
    #ユーザー名
    name = models.CharField(max_length=150, verbose_name='ユーザー名')
    #アクティブフラグ
    is_active = models.BooleanField(default=True, verbose_name='有効')
    #管理者フラグ
    is_admin = models.BooleanField(default=False, verbose_name='管理者')

    objects = UserManager()

    #ID項目にメールアドレスを指定
    USERNAME_FIELD = 'email'
    #必須項目
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):#Trueを返して、権限があることを知らせる
        return True

    def has_module_perms(self, app_label):#Trueを返して、アプリ（App）のモデル（Model）へ接続できるようにする
        return True

    @property
    def is_staff(self):#Trueの場合、Django管理サイトにログインできる
        return self.is_admin