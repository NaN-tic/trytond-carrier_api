import datetime
import unittest
from decimal import Decimal

from proteus import Model
from trytond.modules.company.tests.tools import create_company, get_company
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules


class Test(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):

        today = datetime.date.today()

        # Install carrier_api Module
        activate_modules('carrier_api')

        # Create company
        _ = create_company()
        company = get_company()

        # Create countries
        Country = Model.get('country.country')
        spain = Country()
        spain.name = 'Spain'
        spain.code = 'ES'
        spain.save()

        # Create customer
        Party = Model.get('party.party')
        customer = Party(name='Customer')
        customer.save()
        address, = customer.addresses
        address.postal_code = '08720'
        address.country = spain
        address.save()
        customer2 = Party(name='Customer2')
        customer2.save()
        address2, = customer2.addresses
        address2.postal_code = '08720'
        address2.country = spain
        address2.save()

        # Create category
        ProductCategory = Model.get('product.category')
        category = ProductCategory(name='Category')
        category.save()

        # Create product
        ProductUom = Model.get('product.uom')
        ProductTemplate = Model.get('product.template')
        Product = Model.get('product.product')
        unit, = ProductUom.find([('name', '=', 'Unit')])
        product = Product()
        template = ProductTemplate()
        template.name = 'Product'
        template.default_uom = unit
        template.type = 'goods'
        template.list_price = Decimal('20')
        product, = template.products
        product.cost_price = Decimal('8')
        template.save()
        product, = template.products
        service = Product()
        template = ProductTemplate()
        template.name = 'Service'
        template.default_uom = unit
        template.type = 'service'
        template.list_price = Decimal('20')
        service, = template.products
        service.cost_price = Decimal('8')
        template.save()
        service, = template.products

        # Get stock locations
        Location = Model.get('stock.location')
        warehouse_loc, = Location.find([('code', '=', 'WH')])
        supplier_loc, = Location.find([('code', '=', 'SUP')])
        customer_loc, = Location.find([('code', '=', 'CUS')])
        output_loc, = Location.find([('code', '=', 'OUT')])
        storage_loc, = Location.find([('code', '=', 'STO')])

        # Make 1 unit of the product available
        StockMove = Model.get('stock.move')
        incoming_move = StockMove()
        incoming_move.product = product
        incoming_move.unit = unit
        incoming_move.quantity = 10
        incoming_move.from_location = supplier_loc
        incoming_move.to_location = storage_loc
        incoming_move.planned_date = today
        incoming_move.effective_date = today
        incoming_move.company = company
        incoming_move.unit_price = Decimal('1')
        incoming_move.currency = company.currency
        incoming_move.click('do')

        # Create Shipment Out
        ShipmentOut = Model.get('stock.shipment.out')
        shipment_out = ShipmentOut()
        shipment_out.planned_date = today
        shipment_out.customer = customer
        shipment_out.warehouse = warehouse_loc
        shipment_out.company = company
        shipment_out.outgoing_moves.extend([StockMove(), StockMove()])
        for move in shipment_out.outgoing_moves:
            move.product = product
            move.unit = unit
            move.quantity = 1
            move.from_location = output_loc
            move.to_location = customer_loc
            move.company = company
            move.unit_price = Decimal('1')
            move.currency = company.currency
        shipment_out.save()
        shipment_out.click('wait')
        shipment_out.click('assign_try')
        shipment_out.reload()
        shipment_out.click('pick')
        shipment_out.click('pack')
        self.assertEqual(shipment_out.state, 'packed')
