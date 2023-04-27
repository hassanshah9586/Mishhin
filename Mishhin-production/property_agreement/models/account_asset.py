from odoo import api, fields , models


class PropertyAgreement(models.Model):
    _inherit = 'account.asset'

    partner_id = fields.Many2one(comodel_name="res.partner", string="Landlord")
    commission_type = fields.Selection([('fixed', 'Fixed'), ('percentage', 'Percentage')], string="Type of Commission",
                                       default='fixed')
    commission_percentage = fields.Float(string="Commission %")
    fixed_commission = fields.Float(string="Fixed Commission")

    our_commission_percentage = fields.Float()
    our_fixed_commission = fields.Float()

    our_commission_percent = fields.Float(string="Our Commission %")
    our_commission_fixe = fields.Float(string="Our Fixed Commission")

    is_our_commission_readonly = fields.Boolean()
    is_our_comm_readonly = fields.Boolean()

    our_invoice_read = fields.Boolean(default=False)
    our_fixed_invoice_read = fields.Boolean(default=False)

    our_comp_read = fields.Boolean(default=False)
    our_fixed_comp_read = fields.Boolean(default=False)

    @api.onchange('our_commission_percentage')
    def set_readonly_fields_1(self):
        if self.our_commission_percentage > 0:
            self.our_invoice_read = False
            self.our_fixed_invoice_read = True
        else:
            self.our_invoice_read = False
            self.our_fixed_invoice_read = False

    @api.onchange('our_fixed_commission')
    def set_readonly_fields_2(self):
        if self.our_fixed_commission > 0:
            self.our_invoice_read = True
            self.our_fixed_invoice_read = False
        else:
            self.our_invoice_read = False
            self.our_fixed_invoice_read = False

    @api.onchange('our_commission_percent')
    def set_readonly_fields_3(self):
        if self.our_commission_percent > 0:
            self.our_comp_read = False
            self.our_fixed_comp_read = True
        else:
            self.our_comp_read = False
            self.our_fixed_comp_read = False

    @api.onchange('our_commission_fixe')
    def set_readonly_fields_4(self):
        if self.our_commission_fixe > 0:
            self.our_comp_read = True
            self.our_fixed_comp_read = False
        else:
            self.our_comp_read = False
            self.our_fixed_comp_read = False

    @api.onchange('our_commission_percentage', 'our_fixed_commission')
    def compute_is_commission_readonly(self):
        for rec in self:
            rec.is_our_commission_readonly = False
            rec.is_our_comm_readonly = False
            if rec.our_commission_percentage > 0 or rec.our_fixed_commission > 0:
                # rec.our_commission_percent = 0
                # rec.our_commission_fixe = 0
                rec.is_our_comm_readonly = True

    @api.onchange('our_commission_percent', 'our_commission_fixe')
    def compute_our_commission_readonly(self):
        for rec in self:
            rec.is_our_commission_readonly = False
            rec.is_our_comm_readonly = False
            if rec.our_commission_percent > 0 or rec.our_commission_fixe > 0:
                # rec.our_commission_percentage = 0
                # rec.our_fixed_commission = 0
                rec.is_our_commission_readonly = True

    @api.onchange('commission_type')
    def _setting_commission_values(self):
        self.ensure_one()
        if self.commission_type == 'fixed':
            self.commission_percentage = 0
            # self.our_commission_percentage = 0
            # self.our_commission_percent = 0
        elif self.commission_type == 'percentage':
            self.fixed_commission = 0
            # self.our_fixed_commission = 0
            # self.our_commission_fixe = 0

