# Copyright 2024 Antoni Marroig(APSL-Nagarro)<amarroig@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    # Campo para vínculo bidirecional com MRP
    mrp_production_id = fields.Many2one(
        comodel_name="mrp.production",
        string="Manufacturing Order",
        copy=False,
        readonly=True,
        ondelete="set null",
    )

    def action_view_repair_manufacturing_order(self):
        """Navega para a ordem de produção vinculada"""
        self.ensure_one()
        if not self.mrp_production_id:
            return {"type": "ir.actions.act_window_close"}
        
        return {
            "type": "ir.actions.act_window",
            "res_model": "mrp.production",
            "res_id": self.mrp_production_id.id,
            "view_mode": "form",
            "target": "current",
        }
