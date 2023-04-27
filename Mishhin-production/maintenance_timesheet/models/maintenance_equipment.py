# Copyright 2019 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    def _prepare_project_from_equipment_values(self, values):
        data = super()._prepare_project_from_equipment_values(values)
        data["allow_timesheets"] = True
        return data
