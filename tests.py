import unittest
from sqlalchemy import create_engine
from vatter import db, models


class TestModels(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engine = create_engine('sqlite:///:memory:')
        db.Session.configure(bind=engine)
        models.Base.metadata.create_all(engine)

    def test_customer_add(self):
        session = db.Session()
        new_customer = models.Customer()
        self.assertIsNone(new_customer.id)
        session.add(new_customer)
        session.commit()
        self.assertEqual(new_customer.id, 1)

    def test_invoice_add(self):
        session = db.Session()
        new_invoice = models.Invoice(buyer=models.Customer())
        session.add(new_invoice)
        session.commit()
        self.assertEqual(new_invoice.id, 1)

        invoice = session.query(models.Invoice).first()
        self.assertIsNotNone(invoice.buyer)

    def test_item_add(self):
        session = db.Session()
        invoice = session.query(models.Invoice).first()
        new_item = models.Item(invoice=invoice)
        session.add(new_item)
        session.commit()
        self.assertEqual(new_item.id, 1)
        self.assertEqual(new_item.invoice.id, invoice.id)

    def test_models_count(self):
        session = db.Session()
        invoice = session.query(models.Invoice).first()
        invoice_count = session.query(models.Invoice).count()
        customer_count = session.query(models.Customer).count()
        self.assertEqual(invoice.buyer.id, 2)
        self.assertEqual(invoice_count, 1)
        self.assertEqual(customer_count, 2)


if __name__ == '__main__':
    unittest.main()
