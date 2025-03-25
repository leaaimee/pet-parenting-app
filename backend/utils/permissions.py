from functools import lru_cache
from backend.models.users_models import Users
from backend.utils.constants import AccessLevel
from backend.models.invitations_models import Permissions


@lru_cache(maxsize=1024)
def get_user_permissions(user_id, pet_id):
    override = Permissions.query.filter_by(user_id=user_id, pet_id=pet_id).first()
    if override:
        return AccessLevel[override.access_level].value #what to do when access level changes

    user = Users.query.get(user_id)
    return AccessLevel[user.access_level].value()

def user_has_access(user_id, pet_id, required_permission):
    permissions = get_user_permissions(user_id, pet_id)
    return required_permission in permissions
