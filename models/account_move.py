from odoo import api, fields, models

from .restrictions import forbid_unlink, is_invoicing_only


class AccountMove(models.Model):
    _inherit = 'account.move'

    invoicing_only_user = fields.Boolean(
        string="Invoicing-Only User",
        compute='_compute_invoicing_only_user',
        help="Technical field: True when the current user may not edit a posted invoice.",
    )

    @api.depends_context('uid')
    def _compute_invoicing_only_user(self):
        restricted = is_invoicing_only(self.env)
        for move in self:
            move.invoicing_only_user = restricted

    def _check_access(self, operation):
        return super()._check_access(operation) or forbid_unlink(self, operation)
