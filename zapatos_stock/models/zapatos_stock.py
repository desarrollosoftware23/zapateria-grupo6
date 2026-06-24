from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ZapatoStock(models.Model):
    _inherit = 'zapatos.zapato'

    estado_stock = fields.Selection([
        ('rojo', 'Crítico'),
        ('amarillo', 'Bajo'),
        ('verde', 'Normal'),
    ], compute='_compute_estado_stock', store=True)

    @api.depends('stock', 'stock_minimo')
    def _compute_estado_stock(self):
        for a in self:
            stock = a.stock or 0
            minimo = a.stock_minimo or 5

            if stock <= 0:
                a.estado_stock = 'rojo'
            elif stock <= minimo:
                a.estado_stock = 'amarillo'
            else:
                a.estado_stock = 'verde'

    @api.constrains('precio')
    def _check_precio(self):
        for record in self:
            if record.precio <= 0:
                raise ValidationError('El precio del zapato debe ser mayor que cero.')
            
    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if not record.name or not record.name.strip():
                raise ValidationError('El nombre del zapato es obligatorio.')
            
    @api.constrains('stock')
    def _check_stock(self):
        for record in self:
            if record.stock < 0:
                raise ValidationError('El stock debe ser mayor o igual a 0.')
            if record.stock > 1000:
                raise ValidationError('El stock es demasiado alto.')
            
    @api.constrains('talla')
    def _check_talla(self):
        for record in self:
            if record.talla <= 0:
                raise ValidationError("La talla debe de ser mayor a 0.")
            
    @api.constrains('codigo', 'marca', 'color', 'material')
    def _check_campos_opcionales(self):
        for r in self:
            if not r.codigo:
                raise ValidationError("El código es obligatorio.")
            if not r.marca:
                raise ValidationError("La marca es obligatoria.")
            if not r.color:
                raise ValidationError("El color es obligatorio.")
            if not r.material:
                raise ValidationError("El material es obligatorio.")