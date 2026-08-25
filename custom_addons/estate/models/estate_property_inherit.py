from odoo import models, fields, api


class EstateProperty(models.Model):
    _inherit = "estate.property"

    reference_code = fields.Char(string="Reference Code")

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:
            if not vals.get("reference_code"):
                vals["reference_code"] = self.env["ir.sequence"].next_by_code(
                    "estate.property"
                )

        return super().create(vals_list)
