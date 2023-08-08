from django.contrib import admin
from users.models import User, Invite


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'phone_number',
                    'auth_code',
                    'invite_code',
                    'activated_invite_code')
    list_filter = ('phone_number',)
    empty_value_display = '-пусто-'


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ('invitation_belong_to', 'invited_user')
