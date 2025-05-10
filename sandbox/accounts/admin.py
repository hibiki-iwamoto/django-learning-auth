from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User

class UserCreationForm(forms.ModelForm):
    """ユーザ登録フォームを定義"""

    #パスワードフィールド
    password1 = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    password2 = forms.CharField(label='パスワード（再）', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'name')

    def clean_password2(self):
        """確認用パスワードが合致するかチェック

        Raises:
            ValidationError: パスワード不一致

        Returns:
            str: 確認用パスワード
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("パスワードが一致しません")
        return password2

    def save(self, commit=True):
        """ユーザ情報保管

        Args:
            commit (bool, optional): DBコミットフラグ、デフォルトでTrue

        Returns:
            User: Userインスタンス
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """ユーザー更新フォームを定義"""

    #パスワードは読取専用に設定
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'is_active', 'is_admin')


class UserAdmin(BaseUserAdmin):
    """Django管理サイトの画面を定義"""

    #ユーザー更新フォーム
    form = UserChangeForm
    #ユーザー登録フォーム
    add_form = UserCreationForm

    list_display = ('email', 'name', 'is_active', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('ユーザー名', {'fields': ('name',)}),
        ('権限', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

#Django管理サイトへUserモデルとUserAdminを登録
admin.site.register(User, UserAdmin)
#Django管理サイトからGroupモデルの削除
admin.site.unregister(Group)