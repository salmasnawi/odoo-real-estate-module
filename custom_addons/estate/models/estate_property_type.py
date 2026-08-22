from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence, name"

    sequence = fields.Integer(
        default=10
    )

    name = fields.Char(
        required=True,
    )

    property_ids = fields.One2many(
        "estate.property",
        "property_type_id",
        string="Properties",
    )

    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_type_id",
        string="Offers",
    )

    offer_count = fields.Integer(
        compute="_compute_offer_count",
        string="Offers",
    )


    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)


    def action_view_offers(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Offers",
            "res_model": "estate.property.offer",
            "view_mode": "list,form",
            "domain": [
                ("property_type_id", "=", self.id)
            ],
        }