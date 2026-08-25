from odoo import models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        result = super().action_sold()

        for record in self:
            self.env["account.move"].create({
                "move_type": "out_invoice",
                "partner_id": record.buyer_id.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": f"Property Sale - {record.name}",
                            "quantity": 1,
                            "price_unit": record.selling_price,
                        },
                    )
                ],
            })

        return result