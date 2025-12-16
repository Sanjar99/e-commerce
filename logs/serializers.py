from rest_framework import serializers
from .models import ActivityLog
from accounts.serializers import UserSerializer
from staff.serializers import StaffUserSerializer

# ------------------------------
# ActivityLog Serializer
# ------------------------------
class ActivityLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    staff = StaffUserSerializer(read_only=True)

    class Meta:
        model = ActivityLog
        fields = ['id', 'user', 'staff', 'action', 'meta_json', 'created_at']
        read_only_fields = ['id', 'user', 'staff', 'created_at']

    # Agar API orqali log yaratish kerak bo‘lsa va request.user/staff bilan bog‘lash kerak bo‘lsa:
    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        staff = getattr(request, 'staff', None)  # Agar staff request orqali berilsa
        validated_data['user'] = user if user and not user.is_staff else None
        validated_data['staff'] = staff if staff else None
        return ActivityLog.objects.create(**validated_data)
