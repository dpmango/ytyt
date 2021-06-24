from django.db import transaction
from loguru import logger

from courses.models import Course
from courses_access.models import Access
from dialogs.models import Dialog, DialogMessage
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


@transaction.atomic()
def create_access_for_user(user: User) -> None:
    """
    Функция создает базовые доступы для пользователя:
        1. Триал-доступ к курсу
        2. Назначение преподавателя
        3. Назначение суппорта
        4. Создание диалога с преподавателем
        5. Создание диалога с суппортом
        6. Отправление приветственного сообщения от суппорта
        7. Отправление приветственного сообщения от преподавателя
    :param user: Новый пользователь
    :return:
    """

    course = Course.objects.order_by('id').first()
    if course:
        access, created = Access.objects.get_or_create(
            user=user, course=course, status=Access.COURSE_ACCESS_TYPE_TRIAL
        )
        if created:
            access.set_trial()

    if user.is_staff:
        return

    educator = User.reviewers.get_less_busy_educator()
    user.reviewer = educator

    support = User.supports.get_less_busy_support()
    user.support = support
    user.save()

    if support is not None:
        dialog_with_support = Dialog.objects.create()
        dialog_with_support.with_role = permissions.GROUP_SUPPORT
        dialog_with_support.users.add(user, support)
        dialog_with_support.save()

        DialogMessage.objects.create_hello_support(dialog_with_support, from_user=support, student=user)

    if educator is not None:
        dialog_with_educator = Dialog.objects.create()
        dialog_with_educator.with_role = permissions.GROUP_EDUCATOR
        dialog_with_educator.users.add(user, educator)
        dialog_with_educator.save()

        DialogMessage.objects.create_hello_educator(dialog_with_educator, from_user=educator, student=user)
