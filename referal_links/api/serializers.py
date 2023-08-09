from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializes user's data."""
    invited_users = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id',
                  'phone_number',
                  'invite_code',
                  'activated_invite_code',
                  'invited_users']
        read_only_fields = ['id']
