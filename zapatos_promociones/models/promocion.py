import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ZapatosPromocion(models.Model):
    _name = 'zapatos.promocion'
    _description = 'Promocion de Calzado'
    _order = 'fecha_inicio desc'

    name = fields.Char(string='Nombre de la promocion', required=True)
    codigo_promo = fields.Char(
        string='Codigo',
        required=True,
        copy=False,
        readonly=True,
        default='Nuevo',
    )
    zapato_id = fields.Many2one(
        'zapatos.zapato',
        string='Zapato',
        required=True,
        ondelete='cascade',
    )
    imagen = fields.Image(string='Imagen', max_width=512, max_height=512)
    color = fields.Integer(string='Color')
    nivel_oferta = fields.Selection(
        [
            ('bajo', 'Bajo'),
            ('medio', 'Medio'),
            ('alto', 'Alto'),
        ],
        string='Nivel de oferta',
        default='bajo',
        required=True,
    )
    porcentaje_descuento = fields.Float(
        string='Descuento (%)',
        required=True,
        digits=(5, 2),
    )
    precio_original = fields.Float(
        string='Precio original',
        related='zapato_id.precio',
        store=True,
        digits=(10, 2),
    )
    precio_final = fields.Float(
        string='Precio final',
        compute='_compute_precio_final',
        store=True,
        digits=(10, 2),
    )
    ahorro = fields.Float(
        string='Ahorro',
        compute='_compute_precio_final',
        store=True,
        digits=(10, 2),
    )
    fecha_inicio = fields.Date(
        string='Inicio',
        required=True,
        default=fields.Date.context_today,
    )
    fecha_fin = fields.Date(string='Fin', required=True)
    unidades_disponibles = fields.Integer(
        string='Unidades en promocion',
        required=True,
        default=1,
    )
    descripcion = fields.Text(string='Descripcion')
    validez = fields.Selection(
        [
            ('valida', 'Valida'),
            ('no_valida', 'No valida'),
        ],
        string='Validez',
        compute='_compute_validez',
        store=True,
    )

    _sql_constraints = [
        (
            'codigo_promo_unico',
            'UNIQUE(codigo_promo)',
            'El codigo de promocion ya existe, debe ser unico.',
        ),
        (
            'descuento_rango',
            'CHECK(porcentaje_descuento > 0 AND porcentaje_descuento <= 100)',
            'El descuento debe ubicarse entre 1 y 100 por ciento.',
        ),
        (
            'unidades_positivas',
            'CHECK(unidades_disponibles > 0)',
            'Las unidades en promocion deben ser mayores a cero.',
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('codigo_promo') or vals.get('codigo_promo') == 'Nuevo':
                vals['codigo_promo'] = self.env['ir.sequence'].next_by_code('zapatos.promocion') or 'Nuevo'
        return super().create(vals_list)

    @api.depends('precio_original', 'porcentaje_descuento')
    def _compute_precio_final(self):
        for registro in self:
            descuento = registro.precio_original * (registro.porcentaje_descuento / 100.0)
            registro.ahorro = descuento
            registro.precio_final = registro.precio_original - descuento

    @api.depends('fecha_fin')
    def _compute_validez(self):
        hoy = fields.Date.context_today(self)
        for registro in self:
            if registro.fecha_fin and registro.fecha_fin < hoy:
                registro.validez = 'no_valida'
            else:
                registro.validez = 'valida'

    @api.constrains('name')
    def _check_name(self):
        for registro in self:
            if not registro.name or len(registro.name.strip()) < 3:
                raise ValidationError('El nombre de la promocion debe tener al menos tres caracteres.')

    @api.constrains('codigo_promo')
    def _check_codigo(self):
        patron = re.compile(r'^[A-Z0-9]{4,12}$')
        for registro in self:
            if not patron.match(registro.codigo_promo or ''):
                raise ValidationError(
                    'El codigo generado no cumple el formato esperado de letras mayusculas y numeros.'
                )

    @api.constrains('porcentaje_descuento')
    def _check_descuento(self):
        for registro in self:
            if registro.porcentaje_descuento <= 0 or registro.porcentaje_descuento > 100:
                raise ValidationError('El descuento debe ubicarse entre 1 y 100 por ciento.')

    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas(self):
        for registro in self:
            if registro.fecha_inicio and registro.fecha_fin and registro.fecha_fin < registro.fecha_inicio:
                raise ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio.')

    @api.constrains('unidades_disponibles', 'zapato_id')
    def _check_unidades(self):
        for registro in self:
            if registro.unidades_disponibles <= 0:
                raise ValidationError('Debe registrar al menos una unidad en promocion.')
            if registro.zapato_id and registro.unidades_disponibles > registro.zapato_id.stock:
                raise ValidationError(
                    'Las unidades en promocion no pueden superar el stock disponible del zapato.'
                )

    @api.constrains('imagen')
    def _check_imagen(self):
        for registro in self:
            if not registro.imagen:
                raise ValidationError('Cada promocion debe incluir una imagen del calzado.')
