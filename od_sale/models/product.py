from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    computer_generation = fields.Char(string='Computer Generation')
    category_id = fields.Many2one('product.category', string="Category")
    status = fields.Selection(
        selection=[('unpay', 'Unpay'), ('paid', 'Paid')],
        default='unpay',
        string='Status',
        store=True,
    )

  
    def set_paid(self):
        for order in self:
            order.status = 'paid'



    def set_un_pay(self):
        
        total = 0
        for order in self:
            order.status = 'unpay'
