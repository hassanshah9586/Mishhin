# Copyright 2019 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    project_id = fields.Many2one(comodel_name="project.project")
    task_id = fields.Many2one(comodel_name="project.task")

    @api.model
    def create(self, values):
        """
        We ensure for appropiate project and task for new requests,
        specially the automatically generated ones
        """
        newreq = super().create(values)
        if not newreq.project_id and newreq.property_id:
            newreq.project_id = newreq.property_id.project_id
        if not newreq.task_id and newreq.maintenance_type == "preventive":
            newreq.task_id = newreq.property_id.preventive_default_task_id

        return newreq

    @api.onchange("property_id")
    def onchange_property_id(self):
        if self.equipment_id and self.property_id.project_id:
            self.project_id = self.property_id.project_id
