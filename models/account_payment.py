from odoo import models

from .restrictions import forbid_unlink


class AccountPayment(models.Model):
    _name = 'account.payment'
    _inherit = ['account.payment', 'mconfort.invoicing.only.mixin']

    def _check_access(self, operation):
        return super()._check_access(operation) or forbid_unlink(self, operation)


class AccountPaymentRegister(models.TransientModel):
    _name = 'account.payment.register'
    _inherit = ['account.payment.register', 'mconfort.invoicing.only.mixin']
