from odoo import models, fields, api
from datetime import date

class EventMailer(models.Model):
    _name = 'event.mailer'
    _description = 'Event Mailer'

    name = fields.Char(string='Event Name', required=True)
    event_date = fields.Date(string='Event Date', required=True)
    email_template_id = fields.Many2one(
        'mail.template', string='Email Template', required=True
    )
    active = fields.Boolean(string='Active', default=True)

    def _send_event_emails(self):
        """Gửi email cho các sự kiện đã setup trong model."""
        today = date.today()
        events = self.search([('active', '=', True), ('event_date', '=', today)])
        for event in events:
            # Tìm nhân viên hoặc khách hàng cần gửi mail
            partners = self.env['res.partner'].search([('email', '!=', False)])
            for partner in partners:
                event.email_template_id.send_mail(partner.id, force_send=True)
