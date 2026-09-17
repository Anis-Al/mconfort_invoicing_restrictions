from odoo import models

from .restrictions import forbid_unlink


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def _check_access(self, operation):
        return super()._check_access(operation) or forbid_unlink(self, operation)
