import enum

class RoleType(enum.Enum):
    OWNER = "Owner"
    FAMILY_MEMBER = "Family Member"
    CO_PARENT = "Co-Parent"
    PARTNER = "Partner"
    ROOMMATE = "Roommate"
    NEIGHBOR = "Neighbor"
    SITTER = "Sitter"


class InvitationStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "DECLINED"


class Permission(enum.Enum):
    VIEW_PET_PROFILE = "view_pet_profile"
    VIEW_MEDICAL_RECORDS = "view_medical_records"
    EDIT_PET_INFO = "edit_pet_info"
    EDIT_MEDICAL_RECORDS = "edit_medical_records"
    ASSIGN_ROLES = "assign_roles"
    VIEW_TASKS = "view_tasks"
    ADD_TASKS = "add_tasks"
    COMPLETE_TASKS = "complete_tasks"
    DELETE_PETS = "delete_pets"


class AccessLevel(enum.Enum):
    ADMIN = set(item for item in Permission)
    FULL_ACCESS = {
        Permission.VIEW_PET_PROFILE,
        Permission.VIEW_MEDICAL_RECORDS,
        Permission.EDIT_PET_INFO,
        Permission.EDIT_MEDICAL_RECORDS,
        Permission.VIEW_TASKS,
        Permission.ADD_TASKS,
        Permission.COMPLETE_TASKS,
    }
    VIEW_ALL = {
        Permission.VIEW_PET_PROFILE,
        Permission.VIEW_MEDICAL_RECORDS,
        Permission.VIEW_TASKS,
    }
    VIEW_LIMITED = {
        Permission.VIEW_PET_PROFILE,
    }

    def has_permission(self, perm):
        return perm in self.value


