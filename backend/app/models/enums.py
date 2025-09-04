from enum import Enum


class OrderStatus(str, Enum):

    NEW = "новый"
    CONFIRMED = "подтвержден"
    PREPARING = "готовится"
    READY = "готов"
    COMPLETED = "выполнен"
    CANCELLED = "отменен"
