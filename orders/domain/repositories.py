from abc import abstractmethod, ABC

from django.db.models import QuerySet
from .entities import Order as OrderEntity
from ..infrastructure.models import Order


class BaseOrderRepository(ABC):
    """
    An abstract base class for an order repository.

    This class defines an interface for working with orders, including methods
    for getting, creating, updating, and deleting orders. All methods
    must be implemented in subclasses.

    """
    @abstractmethod
    def get_all(self) -> QuerySet[Order]:
        pass

    @abstractmethod
    def get_by_id(self, order_id: int) -> Order | None:
        pass

    @abstractmethod
    def create(self, order_entity: OrderEntity) -> Order:
        pass

    @abstractmethod
    def update(self, order_id: int, **kwargs) -> Order | None:
        pass

    @abstractmethod
    def delete(self, order_id: int) -> None:
        pass
