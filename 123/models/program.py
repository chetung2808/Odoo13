from odoo import models, fields, api
from datetime import datetime, timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.coupon.program'
    
    # Thêm trường end_sale dạng ngày tháng
    end_sale = fields.Datetime('End Sale Date')
    count_coupon = fields.Integer(string="Total counpon", compute='_get_counpon_count')

    
    # Thêm trường validity_duration
    validity_duration = fields.Integer(string="Validity Duration (days)", compute='_compute_validity_duration', store=True)
    
    @api.depends('coupon_ids')
    def _get_counpon_count(self):
        coupon_data = self.env['sale.coupon'].read_group([('program_id', 'in', self.ids)], ['program_id'], ['program_id'])
        mapped_data = dict([(m['program_id'][0], m['program_id_count']) for m in coupon_data])
        for program in self:
            program.count_coupon = mapped_data.get(program.id, 0)    
    
    @api.depends('end_sale')
    def _compute_validity_duration(self):
        for order in self:
            if order.end_sale:
                # Tính toán độ chênh lệch giữa ngày kết thúc và ngày hôm nay
                today = datetime.today().date()
                end_date = fields.Datetime.from_string(order.end_sale)
                
                # Đặt thời gian kết thúc là 23h 59p 59s 
                end_sale= end_date.replace(hour=23, minute=59, second=59, microsecond=0)
              
                # Tính độ chênh lệch giữa ngày hôm nay và ngày kết thúc
                duration = (end_sale - datetime.combine(today, datetime.min.time())).days
                order.validity_duration = duration
            else:
                order.validity_duration = 0
