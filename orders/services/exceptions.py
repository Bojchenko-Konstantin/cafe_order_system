class OrderServiceError(Exception):
    """Базовое исключение для ошибок, связанных с заказами."""

    pass


class OrderNotFoundError(OrderServiceError):
    """Заказ не найден."""

    pass


class MenuItemNotFoundError(OrderServiceError):
    """Позиция меню не найдена."""

    pass
