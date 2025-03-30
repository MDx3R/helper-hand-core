import contextvars

from .transaction_manager import TransactionManager

current_transaction_manager = contextvars.ContextVar("current_transaction_manager", default=None)

def set_transaction_manager(manager: TransactionManager):
    current_transaction_manager.set(manager)

def get_transaction_manager() -> TransactionManager | None:
    return current_transaction_manager.get()

def reset_transaction_manager():
    current_transaction_manager.set(None)