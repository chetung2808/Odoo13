from odoo import models, fields, api
from datetime import date

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def _send_birthday_emails(self):
        """Gửi email chúc mừng sinh nhật cho nhân viên có sinh nhật hôm nay."""
        today = date.today()
        employees = self.search([('birthday', '!=', False)])
        for employee in employees:
            # Kiểm tra ngày sinh nhật
            if employee.birthday.month == today.month and employee.birthday.day == today.day:
                template = self.env.ref('your_module_name.email_template_birthday')
                if template:
                    template.send_mail(employee.id, force_send=True)
