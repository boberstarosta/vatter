from sqlalchemy import Column, Float, ForeignKey, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, Sequence('customer_id_seq'), primary_key=True)
    name = Column(String(100))
    street_address = Column(String(100))
    postal_code = Column(String(10))
    city = Column(String(50))
    country = Column(String(50))
    tax_id_number = Column(String(20))

    invoices = relationship('Invoice', back_populates='buyer')


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, Sequence('item_id_seq'), primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoice.id'))
    name = Column(String(100))
    quantity = Column(Integer)
    net_price = Column(Float)

    invoice = relationship('Invoice', back_populates='items')


class Invoice(Base):
    __tablename__ = 'invoice'

    id = Column(Integer, Sequence('invoice_id_seq'), primary_key=True)
    buyer_id = Column(Integer, ForeignKey('customer.id'))

    buyer = relationship('Customer', back_populates='invoices')
    items = relationship('Item', back_populates='invoice')
