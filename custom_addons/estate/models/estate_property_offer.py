from odoo import fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float(
        required=True,
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        required=True,
    )

    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
    )

    status = fields.Selection(
        [
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        default="pending",
        copy=False,
    )

    # =========================
    # Actions
    # =========================

    def action_accept(self):
        for record in self:

            if record.property_id.state in ("sold", "cancelled"):
                raise ValidationError(
                    "You cannot accept an offer for a sold or cancelled property!"
                )

            record.status = "accepted"

            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"

        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"

        return True