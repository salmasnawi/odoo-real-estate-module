from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    # =========================
    # Basic Fields
    # =========================

    name = fields.Char(required=True)

    expected_price = fields.Float(required=True)

    selling_price = fields.Float()

    bedrooms = fields.Integer(default=2)

    living_area = fields.Float()

    # =========================
    # Computed Fields
    # =========================

    difference = fields.Float(
        compute="_compute_difference",
        string="Price Difference",
    )

    offer_count = fields.Integer(
        compute="_compute_offer_count",
        string="Offers",
    )

    # =========================
    # Relations
    # =========================

    owner_id = fields.Many2one(
        "res.partner",
        string="Owner",
    )

    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )

    owner_email = fields.Char(
        related="owner_id.email",
        string="Owner Email",
        readonly=True,
    )

    owner_phone = fields.Char(
        related="owner_id.phone",
        string="Owner Phone",
        readonly=True,
    )

    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offers",
    )

    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags",
    )
    property_type_id = fields.Many2one(
    "estate.property.type",
    string="Property Type",
)

    # =========================
    # Status
    # =========================

    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )

    # =========================
    # Compute Methods
    # =========================

    @api.depends("selling_price", "expected_price")
    def _compute_difference(self):
        for record in self:
            record.difference = (
                record.selling_price - record.expected_price
            )

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # =========================
    # Onchange
    # =========================

    @api.onchange("bedrooms")
    def _onchange_bedrooms(self):
        for record in self:
            if record.bedrooms:
                record.living_area = record.bedrooms * 30

    # =========================
    # Constraints
    # =========================

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0:
                raise ValidationError(
                    "Selling Price must be positive!"
                )

    # =========================
    # ORM Overrides
    # =========================

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name"):
                vals["name"] = "New Property"

        return super().create(vals_list)

    def write(self, vals):
        if "state" in vals:
            for record in self:
                new_state = vals["state"]

                if (
                    record.state == "cancelled"
                    and new_state == "sold"
                ):
                    raise ValidationError(
                        "A cancelled property cannot be sold!"
                    )

                if (
                    record.state == "sold"
                    and new_state == "cancelled"
                ):
                    raise ValidationError(
                        "A sold property cannot be cancelled!"
                    )

        if "selling_price" in vals:
            print("Selling price updated!")

        return super().write(vals)

    def unlink(self):
        for record in self:
            if record.state == "sold":
                raise ValidationError(
                    "You cannot delete a sold property!"
                )

        return super().unlink()

    # =========================
    # Action Methods
    # =========================

    def action_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise ValidationError(
                    "A cancelled property cannot be sold!"
                )

            record.state = "sold"

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise ValidationError(
                    "A sold property cannot be cancelled!"
                )

            record.state = "cancelled"

    def action_view_offers(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Offers",
            "res_model": "estate.property.offer",
            "view_mode": "list,form",
            "domain": [
                ("property_id", "=", self.id),
            ],
            "context": {
                "default_property_id": self.id,
            },
        }