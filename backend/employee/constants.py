from django.utils.translation import gettext as _
from core.constants import TextEnum

class TaskStatus(TextEnum):
    NEW = _('task.status.new')
    IN_PROGRESS = _('task.status.in.progress')
    DONE = _('task.status.done')
    CANCELED = _('task.status.canceled')

class WorkShiftStatus(TextEnum):
    DRAFT = _('workshift.status.draft')
    PENDING = _('workshift.status.pending')
    CONFIRMED = _('workshift.status.confirmed')
    CANCELED = _('workshift.status.canceled')

class LeaveDayStatus(TextEnum):
    DRAFT = _('leave.day.status.draft')
    PENDING = _('leave.day.status.pending')
    APPROVED = _('leave.day.status.approved')
    CANCELED = _('leave.day.status.canceled')

class PrepaidStatus(TextEnum):
    DRAFT = _('prepaid.status.draft')
    PENDING = _('prepaid.status.pending')
    APPROVED = _('prepaid.status.approved')
    CANCELED = _('prepaid.status.canceled')

class PayrollStatus(TextEnum):
    DRAFT = _('payment.status.draft')
    PENDING = _('payment.status.pending')
    APPROVED = _('payment.status.approved')
    CANCELED = _('payment.status.canceled')
