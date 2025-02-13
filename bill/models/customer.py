# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _
from odoo.exceptions import ValidationError
import re

class BillCustomer(models.Model):
    _name = "bill.customer"
    _deciption = 'Bill table'
    
    
    name = fields.Char(string="Name", required= True)
    age = fields.Integer(string="Age")
    email=fields.Char(string="Email", required=True)
    phone=fields.Integer(string="Phone", required= True)
    date_of_birth = fields.Datetime(string="Date Of Birth")
    date_buy = fields.Datetime(string='Current DateTime', default=lambda self: fields.Datetime.now())
    amount_total = fields.Float(string='Total Amount', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    street = fields.Char(string='Street')
    line_ids = fields.One2many('bill.line.model', 'bill_id', string='Bill Lines')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    zip = fields.Char(string='ZIP/Postal Code') 
    country_id = fields.Many2one('res.country', string='Country')
    state = fields.Selection(selection=[('draft', 'Draft'), 
                                        ('ordered', 'Ordered'),
                                        ('paid', 'Paid')], string="State", default='draft')
    account_id = fields.Many2one('account.account', string="Account")

    @api.model
    def create(self, vals):
        vals['date_buy'] = fields.Datetime.now()
        return super(BillCustomer, self).create(vals)   
    
    @api.constrains('email')
    def _check_email(self):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        for record in self:
            if record.email and not re.match(email_regex, record.email):
                raise ValidationError("Invalid email address: %s" % record.email)
    

            


    @api.constrains('phone')
    def _check_phone(self):
        """
        Validates phone format after preprocessing.
        """
        phone_regex = r'^\+?[\d\s\-()]{10}$'  # Allow international format
        for record in self:
            if record.phone and not re.match(phone_regex, record.phone):
                raise ValidationError("Invalid phone number: %s" % record.phone)
    
class BillLineModel(models.Model):
    _name = 'bill.line.model'
    _description = 'Bill Line Model'

    bill_id = fields.Many2one('bill.customer', string='Bill', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.pricelist.item', string='Product/Service')
    description = fields.Char(string='Description')
    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)
    

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit
    
    
    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit
            
            
class BillLineModel(models.Model):
    _name = 'bill.line.model'
    _description = 'Bill Line Model'

    bill_id = fields.Many2one('bill.customer', string='Bill', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product/Service', required=True)
    description = fields.Char(string='Description')
    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price', compute='_compute_price_unit', store=True)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """ Automatically set the price unit based on the selected product. """
        if self.product_id:
            self.price_unit = self.product_id.lst_price  # Assuming lst_price is the field for sale price

    def register(cls):
        cls._register()
        cls._register_fields()

    def unregister(cls):
        cls._unregister()
        cls._unregister_fields()
 


