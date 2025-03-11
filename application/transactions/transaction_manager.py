from abc import ABC, abstractmethod

class TransactionManager(ABC):
    """
    Интерфейс для менеджера транзакций.

    Этот класс определяет интерфейс для менеджера транзакций, работающего через асинхронный контекстный менеджер.
    """

    @abstractmethod
    async def __aenter__(self):
        """Начинает транзакцию."""
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Завершает транзакции, выполняя коммит или откат."""
        pass
    
    @abstractmethod
    async def get_session(self):
        """Контекстный менеджер для получения сессии. Использовать вместе с оператором `async with`."""
        pass