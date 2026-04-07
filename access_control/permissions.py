from .models import AccessRule

def check_permission(user, element_name, action, is_owner=False):
    if not user or not user.is_active or not user.role:
        return False
    try:
        rule = AccessRule.objects.get(role=user.role, element__name=element_name)
    except AccessRule.DoesNotExist:
        return False

    if action == 'read':
        return rule.can_read or (rule.can_read_all and not is_owner)
    if action == 'create':
        return rule.can_create
    if action == 'update':
        return rule.can_update or (rule.can_update_all and not is_owner)
    if action == 'delete':
        return rule.can_delete or (rule.can_delete_all and not is_owner)
    if action == 'read_all':
        return rule.can_read_all
    if action == 'update_all':
        return rule.can_update_all
    if action == 'delete_all':
        return rule.can_delete_all
    return False