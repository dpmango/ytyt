from urllib.parse import parse_qs

from channels.auth import AuthMiddleware
from channels.sessions import CookieMiddleware, SessionMiddleware
from loguru import logger
from rest_framework import exceptions

from users.auth import WebSocketJSONWebTokenAuthentication


class JWTAuthMiddleware(AuthMiddleware):

    async def __call__(self, scope, receive, send):
        """
        Переопределенный промежуточный слой доступа к сокету, который параллельно авторизует юзера через JWT
        Так как протокол сокета не поддерживает кастомные заголовки запроса, то токен передается в параметрах
        """
        query_string = scope.get('query_string').decode()
        query_params = parse_qs(query_string)

        wt = WebSocketJSONWebTokenAuthentication()
        scope = dict(scope)

        self.populate_scope(scope)
        await self.resolve_scope(scope)

        try:
            user = await wt.authenticate(query_params)
        except exceptions.AuthenticationFailed:
            logger.debug('Ошибка декодирования токера в сокете, query_params=%s' % query_params)
            return

        scope.update({**query_params, 'user': user})
        return await super().__call__(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    return CookieMiddleware(SessionMiddleware(JWTAuthMiddleware(inner)))
