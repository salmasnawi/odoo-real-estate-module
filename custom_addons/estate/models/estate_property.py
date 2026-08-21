from odoo import api, fields, models
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(required=True)

    expected_price = fields.Float(required=True)

    selling_price = fields.Float()

    difference = fields.Float(
        compute="_compute_difference",
        string="Price Difference"
    )

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


    # Computed Field
    @api.depends('selling_price', 'expected_price')
    def _compute_difference(self):
        for record in self:
            record.difference = (
                record.selling_price - record.expected_price
            )

    # Onchange
    @api.onchange('bedrooms')
    def _onchange_bedrooms(self):
        if self.bedrooms:
            self.living_area = self.bedrooms * 30


    # Constraint
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0:
                raise ValidationError(
                    "Selling Price must be positive!"
                )