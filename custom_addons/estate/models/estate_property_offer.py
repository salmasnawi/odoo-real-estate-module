from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    price = fields.Float(required=True)

    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True
    )
    offer_ids = fields.One2many(
    'estate.property.offer',
    'property_id',
    string='Offers'
)