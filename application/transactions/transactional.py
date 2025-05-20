import functools

from .configuration import get_transaction_manager


def transactional(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        # TODO: После написания тестов убрать self из wrapper и func для поддерджи функций
        manager = get_transaction_manager()
        if not manager:
            raise ValueError("Не установлен менеджер транзакций.")
        async with manager:
            return await func(self, *args, **kwargs)

    return wrapper
