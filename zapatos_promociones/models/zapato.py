from odoo import models, fields, api


class ZapatosZapato(models.Model):
    _inherit = 'zapatos.zapato'

    promocion_ids = fields.One2many(
        'zapatos.promocion',
        'zapato_id',
        string='Promociones',
    )
    promocion_count = fields.Integer(
        string='Numero de promociones',
        compute='_compute_promocion_count',
    )

    @api.depends('promocion_ids')
    def _compute_promocion_count(self):
        for registro in self:
            registro.promocion_count = len(registro.promocion_ids)

    def action_ver_promociones(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Promociones',
            'res_model': 'zapatos.promocion',
            'view_mode': 'kanban,list,form',
            'domain': [('zapato_id', '=', self.id)],
            'context': {'default_zapato_id': self.id},
        }
