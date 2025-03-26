from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class EstatePropertyOfferTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(EstatePropertyOfferTestCase, cls).setUpClass()
        cls.properties = cls.env['estate.property'].create([
            {'name': 'Villa with garden', 'expected_price': 100000, 'state': 'sold'},
            {'name': 'Apartment with view', 'expected_price': 50000, 'state': 'new'},
            {'name': 'House', 'expected_price': 75000, 'state': 'offer_accepted'},
        ])

    def test_create_offer_on_sold_property(self):
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'property_id': self.properties[0].id,
                'price': 90000,
                'validity': 7,
                'partner_id': self.env.ref('base.res_partner_12').id,
            })

    def test_mark_property_as_sold_without_accepted_offer(self):
        with self.assertRaises(UserError):
            self.properties[1].sold_property()
            
    def test_mark_property_as_sold_with_accepted_offer(self):
        self.properties[2].sold_property()
        self.assertEqual(self.properties[2].state, 'sold')