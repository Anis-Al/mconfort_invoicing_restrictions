from odoo import api, fields, models
from odoo.exceptions import AccessError

RESTRICTED_GROUP = 'account.group_account_invoice'
PRIVILEGED_GROUP = 'account.group_account_user'


def is_invoicing_only(env):
    return (
        not env.su
        and env.user.has_group(RESTRICTED_GROUP)
        and not env.user.has_group(PRIVILEGED_GROUP)
    )


def forbid_unlink(records, operation):
    if operation == 'unlink' and is_invoicing_only(records.env):
        description = records._description
        return records, lambda: AccessError(records.env._(
            "Invoicing users are not allowed to delete %(model)s records.",
            model=description,
        ))
    return None


class InvoicingOnlyMixin(models.AbstractModel):
    _name = 'mconfort.invoicing.only.mixin'
    _description = "Invoicing-Only User Flag"

    invoicing_only_user = fields.Boolean(
        string="Invoicing-Only User",
        compute='_compute_invoicing_only_user',
        help="Technical field: True when the current user is an Invoicing-only user.",
    )

    @api.depends_context('uid')
    def _compute_invoicing_only_user(self):
        restricted = is_invoicing_only(self.env)
        for record in self:
            record.invoicing_only_user = restricted
