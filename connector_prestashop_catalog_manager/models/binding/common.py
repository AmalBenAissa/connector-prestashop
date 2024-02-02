# Copyright 2021 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class PrestashopBinding(models.AbstractModel):
    _inherit = "prestashop.binding"

    @api.model
    def create(self, vals):
        return super(
            PrestashopBinding,
            self.with_context(catalog_manager_ignore_translation=True),
        ).create(vals)
