from enum import Enum
from django.utils.translation import gettext as _

class TextEnum(Enum):
    @classmethod
    def choices(cls, excludes=[]):
        return [(x.name, x.value) for x in cls if x.name not in excludes]

class Gender(TextEnum):
    MALE = _('gender.male')
    FEMALE = _('gender.female')
    OTHER = _('gender.other')
    UNKNOWN = _('gender.unknown')

class BaseStatus(TextEnum):
    DRAFT = _('status.draft')
    ACTIVE = _('status.active')
    INACTIVE = _('status.inactive')

class PartnerType(TextEnum):
    CUSTOMER = _('partner.type.customer')
    COMPANY = _('partner.type.company')
    AGENT = _('partner.type.agent')

class CodeSystemStatus(TextEnum):
    DRAFT = _('codesystem.status.draft')
    ACTIVE = _('codesystem.status.active')
    RETIRED = _('codesystem.status.retired')

class CodeSystemDataType(TextEnum):
    INTEGER = _('codesystem.datatype.int')
    FOREIGN_KEY = _('codesystem.datatype.foreign.key')
    MANY_TO_MANY_FIELD = _('codesystem.datatype.manytomany.field')
    BOOLEAN = _('codesystem.datatype.boolean')
    FLOAT = _('codesystem.datatype.float')
    DATE = _('codesystem.datatype.date')
    DATETIME = _('codesystem.datatype.datetime')
    STRING = _('codesystem.datatype.string')