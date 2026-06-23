from odoo import models, fields, api
         
class Etiquetas(models.Model):
    _name = 'etiquetas.etiquetas'
    _description = 'Modelo para gestionar etiquetas'

    name = fields.Char(string='Nombre', required=True)
    color = fields.Char(string='Color de la Etiqueta', default='#000000')
    zapato_ids = fields.Many2many('zapatos.zapato', string='Zapatos Relacionados')
    
    
# Herencia del modelo zapato para agregar descuento, precio final y etiquetas
class ZapatoExtension(models.Model):
    _inherit = 'zapatos.zapato'

    descuento = fields.Float(string='Descuento (%)')
    precio_final = fields.Float(
        string='Precio Final',
        compute='_compute_precio_final',
        store=True
    )
    etiqueta_ids = fields.Many2many('etiquetas.etiquetas', string='Etiquetas')

    @api.depends('precio', 'descuento')
    def _compute_precio_final(self):
        for record in self:
            record.precio_final = record.precio - (record.precio * record.descuento / 100)

