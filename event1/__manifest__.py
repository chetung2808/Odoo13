{
    'name': 'Event and Birthday Email Automation',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Automate event emails and birthday greetings for employees and customers.',
    'description': """
        This module allows:
        - Automated email sending for custom events like Noel or Tet.
        - Automated birthday greetings for employees without setup.
    """,
    'author': 'CMT',
    'website': 'https://aldoshoes.com',
    'depends': ['base', 'mail', 'hr'],  
    'data': [
        'data/email_templates.xml',  
        'views/event.xml',        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
