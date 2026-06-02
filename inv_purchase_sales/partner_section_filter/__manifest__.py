{
    'name': 'Partner Section Filter',
    'version': '18.0.1.0.0',
    'summary': 'Show only customers in Customers and only vendors in Vendors; hide employees',
    'description': """
        - Customers menu: partners with customer rank only (no vendors-only, no employees)
        - Vendors menu: partners with supplier rank only (no employees)
        - Employee work contacts and employee-flagged partners are excluded from both
    """,
    'author': 'Niyat Consultancy.',
    'category': 'Sales/CRM',
    'depends': ['contacts', 'account', 'hr'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
