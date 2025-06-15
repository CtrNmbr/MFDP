from enum import Enum

class TaskStatus(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"

class TransactionType(str, Enum):
    DEPOSIT = ("DEPOSIT",)
    PAYMENT = ("PAYMENT",)  # оплата вызова модели
    WITHDRAW = ("WITHDRAW",)  # возвраты, вывод средств со счета

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"