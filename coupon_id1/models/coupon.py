from odoo import models, fields, _
from odoo.tools import safe_eval
from odoo.exceptions import ValidationError


class SaleCouponGenerate(models.TransientModel):
    _inherit = 'sale.coupon.generate'

    header_code = fields.Char(string="custom coupon")
    length = fields.Integer(string="Length coupon")
    position = fields.Integer(string="Postion add custom coupon")
    def generate_coupon(self):
        program = self.env['sale.coupon.program'].browse(self.env.context.get('active_id'))
        vals = {'program_id': program.id}
        if self.length <= 0:
            raise ValidationError(_('Coupon length must be greater than 0.'))
          
        header_code = self.header_code  

        if self.generation_type == 'nbr_coupon' and self.nbr_coupons > 0:
            for count in range(0, self.nbr_coupons):
              
                coupon = self.env['sale.coupon'].create(vals)
                 
                coupon_code_length = len(coupon.code)  
                if self.length < coupon_code_length:
                    coupon.code = coupon.code[:self.length]
                else:
                    coupon.code = coupon.code.ljust(self.length, '0')
                 
                if hasattr(coupon, 'code'):
                    position = min(self.position - 1, len(coupon.code))  # Đảm bảo không vượt quá chiều dài chuỗi
                    coupon.code = coupon.code[:position] + header_code + coupon.code[position:]
                else:
                    coupon.code = f"{header_code}{count}"


        if self.generation_type == 'nbr_customer' and self.partners_domain:
            for partner in self.env['res.partner'].search(safe_eval(self.partners_domain)):
                vals.update({'partner_id': partner.id})
                coupon = self.env['sale.coupon'].create(vals)
                
         
                coupon_code_length = len(coupon.code)  
                if self.length < coupon_code_length:
                    coupon.code = coupon.code[:self.length]
                else:
                    coupon.code = coupon.code.ljust(self.length, '0')
                    
                if hasattr(coupon, 'code'):
                    position = min(self.position - 1, len(coupon.code))  # Đảm bảo không vượt quá chiều dài chuỗi
                    coupon.code = coupon.code[:position] + header_code + coupon.code[position:]
                else:
                    coupon.code = f"{header_code}{count}"
                    
                context = dict(lang=partner.lang)
                subject = _('%s, a coupon has been generated for you') % (partner.name)
                del context
                template = self.env.ref('sale_coupon.mail_template_sale_coupon', raise_if_not_found=False)
                if template:
                    template.send_mail(coupon.id, email_values={'email_from': self.env.user.email or '', 'subject': subject})
