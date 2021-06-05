from django.db import transaction
from loguru import logger

from dialogs.models import Dialog
from users import permissions
from users.models import User


@transaction.atomic()
def replace_educator_to_reviewer(user: User) -> None:
    """
    Функция шорткат для переназначения наставника на ревьюера у пользователя
    :param user: Объект пользователя, которому нужно переназначить ревьюера
    :return: None
    """
    dialog = Dialog.objects.get_dialog_with_educator(user)
    if not dialog:
        logger.error('[does not exists dialog] user=%s' % (user.id, ))
        return

    new_reviewer = User.reviewers.get_less_busy()

    dialog.users.remove(user.reviewer)
    dialog.users.add(new_reviewer)
    dialog.with_role = permissions.GROUP_MENTOR
    dialog.save()

    user.reviewer = new_reviewer
    user.save()
