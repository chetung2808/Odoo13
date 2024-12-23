{
    'name': 'Partner API Integration',
    'version': '1.0',
    'category': 'Contacts',
    'summary': 'Fetch and update res.partner records using an external API',
    'depends': ['base', 'contacts'],
    'data': [
        'views/partner_api_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
