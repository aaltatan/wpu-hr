from django.utils.translation import gettext_lazy as _

MESSAGES = {
  'success': _('Done! 😁'),
  'cannot_delete_faculty': _('You can\'t delete this faculty because it has one or more specialties related'),
  'cannot_delete_specialty': _('You can\'t delete this specialty because it has one or more staff related')
}