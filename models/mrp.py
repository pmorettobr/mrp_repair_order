# Copyright 2024 Antoni Marroig(APSL-Nagarro)<amarroig@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class MRPProduction(models.Model):
    _inherit = "mrp.production"

    repair_id = fields.Many2one(
        comodel_name="repair.order",
        string="Repair Order",
        copy=False,
        readonly=True,
        ondelete="set null",
    )

    def action_create_repair_order(self):
        """Cria uma ordem de reparo a partir da ordem de produção"""
        self.ensure_one()
        
        # Carrega a ação padrão do módulo repair
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "repair.action_repair_order_form"
        )
        
        # Configura a ação para modo formulário
        action.update({
            "view_mode": "form",
            "views": [(False, "form")],
            "target": "new",  # Abre em modal
            "name": _("Create Repair Order"),
            "context": {
                "default_product_id": self.product_id.id,
                "default_product_qty": self.product_qty,
                "default_product_uom": self.product_uom_id.id,
                "default_location_id": self.location_dest_id.id,
                # Vínculo bidirecional: ao salvar o repair, define repair_id na MO
                "default_mrp_production_id": self.id,
            },
        })
        return action

    def action_view_mrp_production_repair_orders(self):
        """Navega para a ordem de reparo vinculada"""
        self.ensure_one()
        if not self.repair_id:
            return {"type": "ir.actions.act_window_close"}
        
        return {
            "type": "ir.actions.act_window",
            "res_model": "repair.order",
            "res_id": self.repair_id.id,
            "view_mode": "form",
            "target": "current",
        }
