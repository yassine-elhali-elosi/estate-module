from odoo.tests.common import TransactionCase, Form
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

    def test_onchange_garden_reset(self):
        property_form = Form(self.env['estate.property'])

        property_form.garden = True
        self.assertEqual(property_form.garden_area, 10)
        self.assertEqual(property_form.garden_orientation, 'north')

        property_form.garden_area = 50
        property_form.garden_orientation = 'south'

        self.assertEqual(property_form.garden_area, 50)
        self.assertEqual(property_form.garden_orientation, 'south')

        property_form.garden = False
        self.assertEqual(property_form.garden_area, 0)
        self.assertFalse(property_form.garden_orientation)