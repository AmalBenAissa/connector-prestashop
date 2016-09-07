# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockLocation(models.Model):
    _inherit = 'stock.location'
    
    prestashop_synchronized = fields.Boolean(
       string='Sync with PrestaShop',
       help='Check this option to synchronize this location with PrestaShop')
    
    @api.model
    def get_prestashop_stock_locations(self):
        prestashop_locations = self.search([
           ('prestashop_synchronized', '=', True),
           ('usage', '=', 'internal'),
        ])
        return prestashop_locations


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def update_prestashop_quantities(self):
        for move in self:
            move.product_id.update_prestashop_qty()

    def _recompute(self):
        locations = self.location_id.get_prestashop_stock_locations()
        self.filtered(
            lambda x: (x.location_dest_id.id in locations.ids or
                       x.location_id.id in locations.ids)
        ).update_prestashop_quantities()

    @api.multi
    def action_cancel(self):
        res = super(StockMove, self).action_cancel()
        if res:
            self._recompute()
        return res

    @api.multi
    def action_done(self):
        res = super(StockMove, self).action_done()
        if res:
            self._recompute()
        return res
