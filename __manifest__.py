{
    'name': 'Invoicing Group Restrictions',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Lock posted invoice dates, hide Reset to Draft and forbid deletion for Invoicing-only users',
    'author': 'Anis Alim',
    'depends': ['account'],
    'data': [
        'views/account_move_views.xml',
        'views/account_payment_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
