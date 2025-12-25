from rest_framework import permissions

# ------------------------------
# Basic Role Checks
# ------------------------------
def has_role(user, role_name):
    return hasattr(user, 'staffuser') and user.staffuser.role.name == role_name


class IsSuperAdmin(permissions.BasePermission):
     """Foydalanuvchi Super Admin bo‘lishi kerak"""
    # def has_permission(self, request, view):
    #     return has_role(request.user, 'super_admin')
class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        print(f"DEBUG: User authenticated: {request.user.is_authenticated}")
        print(f"DEBUG: User is_superuser: {request.user.is_superuser}")
        print(f"DEBUG: User: {request.user}")
        return request.user.is_authenticated and request.user.is_superuser

class IsCategoryManager(permissions.BasePermission):
    """Foydalanuvchi Category Manager bo‘lishi kerak"""
    def has_permission(self, request, view):
        return has_role(request.user, 'category_manager')


class IsProductModerator(permissions.BasePermission):
    """Foydalanuvchi Product Moderator bo‘lishi kerak"""
    def has_permission(self, request, view):
        return has_role(request.user, 'product_moderator')


class IsOrderManager(permissions.BasePermission):
    """Foydalanuvchi Order Manager bo‘lishi kerak"""
    def has_permission(self, request, view):
        return has_role(request.user, 'order_manager')


class IsFinanceManager(permissions.BasePermission):
    """Foydalanuvchi Finance Manager bo‘lishi kerak"""
    def has_permission(self, request, view):
        return has_role(request.user, 'finance_manager')


class IsSupportAgent(permissions.BasePermission):
    """Foydalanuvchi Support Agent bo‘lishi kerak"""
    def has_permission(self, request, view):
        return has_role(request.user, 'support_agent')


class IsLogisticsAgent(permissions.BasePermission):
    """Foydalanuvchi Logistics Agent bo‘lishi kerak"""
    def has_permission(self, request, view):
        return has_role(request.user, 'logistics_agent')


class IsStaff(permissions.BasePermission):
    """Har qanday staff userlar (general staff ham)"""
    def has_permission(self, request, view):
        return hasattr(request.user, 'staffuser')


# ------------------------------
# Advanced: Staff or Owner (Oddiy user)
# ------------------------------
class IsStaffOrOwner(permissions.BasePermission):
    """
    StaffUser bo‘lgan userlar hamma ob’ektlarni ko‘radi,
    Oddiy user faqat o‘z ob’ektlarini (masalan ticket) ko‘radi
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'staffuser'):
            return True
        return getattr(obj, 'user', None) == request.user

class IsProductModeratorOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            hasattr(request.user, 'staffuser') and
            request.user.staffuser.role.name in ['product_moderator', 'super_admin']
        )