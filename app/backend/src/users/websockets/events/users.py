from users.models import User


class UserEvent:

    EVENT_USERS_STATUS_ONLINE = 'users.status.online'
    EVENTS = (
        (EVENT_USERS_STATUS_ONLINE, 'Онлайн статус пользователя')
    )

    @staticmethod
    def get_related_users(user: User, **kwargs) -> set:
        """
        Метод получает всех пользователей, с которыми связан пользователем посредством диалогов
        :param user: Пользователь, который меняет статус
        :param kwargs: Дополниетльные аргументы
        """
        dialogs = user.dialog_users_set.all().prefetch_related('users')
        return {us for dialog in dialogs for us in dialog.users.all() if us.id != user.id}

    def get_user_status_online(self, user: User, **kwargs) -> dict:
        """
        Искусственный вызов события для получения статуса онлайн пользователя
        :param user: Пользователь
        """
        data = self._users_status_online(user=user, **kwargs)
        data = data.get('data')

        return {'data': data, 'event': self.EVENT_USERS_STATUS_ONLINE}

    @staticmethod
    def _users_status_online(user: User, **kwargs) -> dict:
        """
        Метод получает статус онлайн пользователя в нужном формате
        :param user: Пользователь
        :param kwargs: Дополнительные аргументы
        """
        return {
            'to': user,
            'data': {
                'status_online': User.objects.check_status_online(user.id),
                'user_id': user.id
            }
        }
