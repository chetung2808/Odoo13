from odoo import models, fields, api
from datetime import date

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    age = fields.Integer(string="Age", compute="_compute_age", stored=True)
    email_template_id = fields.Many2one(
        'mail.template', string='Email Template', required=True
    )

    
    api.depends('birthday')
    def _compute_age(self):
        today=date.today()
        for partner in self:
            if partner.birthday:
                partner.age = today.year - partner.birthday.year - ( (today.month, today.day) < (partner.birthday.month, partner.birthday.day) )
            else:
                partner.age=0
    
    def _send_birthday_emails(self):
        """Gửi email chúc mừng sinh nhật cho nhân viên có sinh nhật hôm nay."""
        today = date.today()
        employees = self.search([('birthday', '!=', False)])
        for employee in employees:
            # Kiểm tra ngày sinh nhật
            if employee.birthday.month == today.month and employee.birthday.day == today.day:
                template = self.env.ref('emp_birth.email_template_birthday')
                if template:
                    template.send_mail(employee.id, force_send=True)