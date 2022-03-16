from typing import List, Optional

from sqlalchemy import select

from classic.components import component
from classic.sql_storage import BaseRepository

from chat_backend.application import interfaces
from chat_backend.application.dataclasses import Cart, Customer, Order, Product

# @component
# class CustomersRepo(BaseRepository, interfaces.CustomersRepo):
#     def get_by_id(self, id_: int) -> Optional[Customer]:
#         query = select(Customer).where(Customer.id == id_)
#         return self.session.execute(query).scalars().one_or_none()
#
#     def add(self, customer: Customer):
#         self.session.add(customer)
#         self.session.flush()
#
#     def get_or_create(self, id_: Optional[int]) -> Customer:
#         if id_ is None:
#             customer = Customer()
#             self.add(customer)
#         else:
#             customer = self.get_by_id(id_)
#             if customer is None:
#                 customer = Customer()
#                 self.add(customer)
#
#         return customer