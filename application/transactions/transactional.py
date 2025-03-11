from .transaction_manager import TransactionManager

def transactional(transaction_manager: TransactionManager):
    def decorator(func):
        async def wrapper(self, *args, **kwargs):
            async with transaction_manager:
                return await func(self, *args, **kwargs)
        return wrapper
    return decorator