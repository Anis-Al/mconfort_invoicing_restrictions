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
