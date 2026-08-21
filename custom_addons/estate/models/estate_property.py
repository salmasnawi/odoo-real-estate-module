from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(required=True)

    expected_price = fields.Float(required=True)

    bedrooms = fields.Integer(default=2)

    living_area = fields.Float()

    owner_id = fields.Many2one(
        'res.partner',
        string='Owner'
    )

    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers'
    )

    tag_ids = fields.Many2many(
        'estate.property.tag',
        string='Tags'
    )

    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        required=True,
        copy=False,
        default='new'
    )