{
    'name': 'zapatos_promociones',
    'version': '1.0',
    'summary': 'Gestion de promociones para la zapateria',
    'description': 'Extension del modulo zapatos para administrar promociones de calzado con imagenes, colores, validez y validaciones por campo.',
    'author': 'LUCIANNY HENRIQUEZ',
    'category': 'Sales',
    'license': 'LGPL-3',
    'depends': ['zapatos'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_promocion.xml',
        'views/promocion_views.xml',
        'views/zapato_views.xml',
    ],
    'installable': True,
    'application': True,
}
