from odoo import models, fields, api


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    is_property = fields.Boolean(string='Is Property Maintenance')
    is_product = fields.Boolean(string='Is Product Maintenance')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity')
    scrap_id = fields.Many2one('stock.scrap', string='Scrap Id')
    is_scrap = fields.Boolean(String='Scrap or not', copy=False)

    @api.onchange('stage_id')
    def create_scrap(self):
        for rec in self:
            if rec.stage_id.name == 'Scrap':
                print("rec", rec)
                scrap = self.env['stock.scrap'].create({
                    'product_id': rec.product_id.id,
                    'scrap_qty': rec.quantity,
                    'origin': rec.name,
                    'product_uom_id': rec.product_id.uom_id.id,
                })
                rec.scrap_id = scrap.id
                rec.is_scrap = True
                scrap.action_validate()

    def get_scrap_orders(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Scrap Orders',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.scrap',
            'res_id': self.scrap_id.id,
            'domain': [('origin', '=', self.name)],
            'context': "{'create': False ,}"
        }
        
