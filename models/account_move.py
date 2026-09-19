from odoo import models

from .restrictions import forbid_unlink


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'mconfort.invoicing.only.mixin']

    def _check_access(self, operation):
        return super()._check_access(operation) or forbid_unlink(self, operation)
