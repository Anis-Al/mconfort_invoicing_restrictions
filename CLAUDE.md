# mconfort_invoicing_restrictions

Odoo 19 module, author Anis Alim, installed on `mconfort`.

Restricts users of the **Invoicing** group (`account.group_account_invoice`) who are
**not** Bookkeeper/Administrator (`account.group_account_user`, implied by
`account.group_account_manager`).

| Target | Restriction |
|---|---|
| `account.move` form | `button_draft` (Reset to Draft) visible to `account.group_account_user` only |
| `account.move` form + invoice list | `invoice_date_due` readonly when `state == 'posted'` |
| `account.payment` form | `action_draft` (Reset to Draft) visible to `account.group_account_user` only |
| `account.move`, `account.payment` | deletion denied (server-side + Delete action hidden) |

## Code notes

Notes that would otherwise live as comments in the source.

### `models/restrictions.py`

- `is_invoicing_only(env)` — True for a user in the Invoicing group without the
  Bookkeeper/Administrator rights. `env.su` short-circuits so sudo/internal code is
  never blocked.
- `forbid_unlink(records, operation)` — `_check_access` helper: denies deletion to
  Invoicing-only users. Returns the `(records, error_factory)` pair `_check_access`
  expects, or `None` when the operation is allowed.
- Denying in `_check_access` rather than in `unlink()` also hides the Delete action in
  the web client: `ir.ui.view._postprocess_access_rights` sets `delete="False"` on the
  root node from `model.has_access('unlink')`
  (`odoo/addons/base/models/ir_ui_view.py:1367`).
- ACLs were rejected for this: `account.access_account_move_uinvoice` is the *only*
  ACL granting `unlink` on `account.move` to accounting users, and Bookkeeper/Admin
  inherit it through group implication — flipping `perm_unlink` there would remove
  delete for everyone. `purchase.access_account_move` also grants `unlink`, so the ACL
  union leaks anyway. `_check_access` is evaluated per user, whatever the ACL union
  says.

### `models/account_move.py`

- `invoicing_only_user` — technical non-stored compute, `@api.depends_context('uid')`.
  It exists because view `readonly`/`invisible` expressions cannot test group
  membership; the client evaluates them against record values only.

### `views/account_move_views.xml`

- `invoice_date` and `delivery_date` are **already** `readonly="state != 'draft'"` in
  the core view (`account/views/account_move_views.xml:1030`, `:1036`, `:1074`,
  `:1502`, and `:482`/`:531` in the lists), for every user — nothing to add.
  `invoice_date_due` (`:1062`, `:534`) is the only one of the three left editable once
  posted, so it is the only one this module touches.
- `button_draft`/`action_draft` carry `groups="account.group_account_invoice"` in core;
  the override narrows them to `account.group_account_user`, matching the pattern of
  the sibling module `account_hide_cancel_invoicing`.

## Known limits

- Neither `account.move` nor `account.payment` has an `active` field, so **archiving
  does not exist** on these models for any user — nothing to restrict.
- The readonly on `invoice_date_due` is a UI rule; an Invoicing user can still change
  it through RPC/import. Add a `write()` guard if that matters.
- The delete denial is absolute for those users, including deletions triggered
  indirectly by a flow they run in their own name (e.g. removing a bank statement
  line, which unlinks its move). Sudo'd internal code is unaffected.

## Commands

```powershell
& "C:\Program Files\Odoo 19.0.20260724\python\python.exe" `
  "C:\Program Files\Odoo 19.0.20260724\server\odoo-bin" `
  -c "C:\Program Files\Odoo 19.0.20260724\server\odoo.conf" `
  -d mconfort -u mconfort_invoicing_restrictions --stop-after-init --no-http --logfile=- --log-level=warn
```

Tests (2, passing): add `--test-enable --test-tags /mconfort_invoicing_restrictions`.
`--logfile=-` prints nothing through the PowerShell tool — write to a file and read it.
