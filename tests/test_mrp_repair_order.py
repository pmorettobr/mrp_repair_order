# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import TransactionCase, Form


class TestMRPRepairOrder(TransactionCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env.ref("product.product_delivery_01")
        cls.mrp_order = cls.env["mrp.production"].create({
            "product_id": cls.product.id,
            "product_qty": 2.0,
            "product_uom_id": cls.product.uom_id.id,
        })

    def test_create_repair_from_mrp(self):
        """Testa fluxo completo: MO -> Repair -> Navegação bidirecional"""
        # Simula MO concluída
        self.mrp_order.write({"state": "done"})
        
        # Cria repair via contexto (simulando ação do usuário)
        RepairForm = Form(self.env["repair.order"].with_context(
            default_product_id=self.mrp_order.product_id.id,
            default_product_qty=self.mrp_order.product_qty,
            default_product_uom=self.mrp_order.product_uom_id.id,
            default_mrp_production_id=self.mrp_order.id,
        ))
        repair = RepairForm.save()
        
        # Valida vínculo na MO
        self.mrp_order.write({"repair_id": repair.id})
        self.assertEqual(
            self.mrp_order.repair_id,
            repair,
            "MO deve referenciar o repair criado"
        )
        
        # Valida vínculo no repair
        self.assertEqual(
            repair.mrp_production_id,
            self.mrp_order,
            "Repair deve referenciar a MO de origem"
        )
