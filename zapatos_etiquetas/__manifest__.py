{
    'name': 'zapatos_etiquetas_descuentos',
    'version': '1.0',
    'summary': 'Extensión de zapatos para agregar etiquetas y descuentos',
    'description': 'Este módulo extiende el módulo de zapatos para agregar campos de etiquetas y descuentos a los productos.',
    'author': 'Nicole.R',
    'category': 'Sales',
    'license': 'LGPL-3',
    'depends': ['zapatos'],
    'data': [
        
        'security/ir.model.access.csv',
        'views/etiqueta_descuento_views.xml',
    ],
    'installable': True,
    'application': True,
}
