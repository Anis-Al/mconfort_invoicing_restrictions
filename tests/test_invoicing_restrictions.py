from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestInvoicingRestrictions(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        groups = cls.env.ref('base.group_user') + cls.env.ref('account.group_account_invoice')
        cls.invoicing_user = cls.env['res.users'].create({
            'name': 'Invoicing Only',
            'login': 'invoicing_only_test',
            'group_ids': [(6, 0, groups.ids)],
        })
        cls.partner = cls.env['res.partner'].create({'name': 'Restriction Test Partner'})
        cls.invoice = cls.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': cls.partner.id,
            'invoice_line_ids': [(0, 0, {'name': 'Line', 'quantity': 1, 'price_unit': 100.0})],
        })

    def test_invoicing_user_cannot_delete(self):
        invoice = self.invoice.with_user(self.invoicing_user)
        self.assertFalse(invoice.has_access('unlink'))
        self.assertTrue(invoice.has_access('write'))
        self.assertTrue(invoice.invoicing_only_user)
        with self.assertRaises(AccessError):
            invoice.unlink()
        self.assertFalse(self.env['account.payment'].with_user(self.invoicing_user).has_access('unlink'))
        for model in ('account.payment', 'account.payment.register'):
            self.assertTrue(self.env[model].with_user(self.invoicing_user).new({}).invoicing_only_user)

    def test_bookkeeper_keeps_delete(self):
        self.invoicing_user.group_ids = [(4, self.env.ref('account.group_account_user').id)]
        invoice = self.invoice.with_user(self.invoicing_user)
        self.assertTrue(invoice.has_access('unlink'))
        self.assertFalse(invoice.invoicing_only_user)
        self.assertFalse(self.env['account.payment.register'].with_user(self.invoicing_user).new({}).invoicing_only_user)
