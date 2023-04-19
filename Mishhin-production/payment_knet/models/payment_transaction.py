# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

import logging
from werkzeug.urls import url_decode

from odoo import _, api, fields, models
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.tools.float_utils import float_compare

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    knet_tx_resp = fields.Char(string="Encrypted Transaction Response", groups='base.group_user')
    knet_tx_id = fields.Char(string="KNET Transaction ID")
    knet_reference_id = fields.Char(string="KNET Reference ID")

    @api.model
    def _knet_form_get_tx_from_data(self, data):
        reference = data.get('trackid')
        if not reference:
            raise ValidationError("KNET: " + _("Received data with missing reference %s." % reference))
        tx = self.search([('reference', '=', reference)])
        if not tx or len(tx) > 1:
            error_msg = 'KNET: received data for reference %s' % (reference)
            if not tx:
                error_msg += ': no order found'
            else:
                error_msg += ': multiple order found'
            _logger.info(error_msg)
            raise ValidationError(error_msg)
        return tx

    def _knet_form_get_invalid_parameters(self, data):
        data = self.acquirer_id.decrypt(data.get("trandata"))
        data = url_decode(data)
        invalid_parameters = []
        if not data.get("ErrorText") and not data.get("Error"):
            result = data.get("result")
            if result != "CANCELED":
                if float_compare(float(data.get('amt', '0.00')), self.amount, 2) != 0:
                    invalid_parameters.append(('Amount', data.get('amt'), '%.3f' % self.amount))
        return invalid_parameters

    def _knet_form_validate(self, data):
        self.write({
            'acquirer_reference': data.get('paymentid'),
            'knet_tx_resp': data.get("trandata")
        })

        if data.get("ErrorText") or data.get("Error"):
            error = _("KNET: Gateway did not approve the payment:\n%s" % data.get("ErrorText"))
            _logger.error(error)
            self._set_transaction_error(error)

        data = self.acquirer_id.decrypt(data.get("trandata"))
        data = url_decode(data)
        result = data.get("result")
        if result == "CANCELED":
            _logger.info(_("KNET payment cancelled for tx %s" % self.reference))
            self._set_transaction_cancel()
        else:
            self.write({
                'knet_tx_id': data['tranid'],
                'knet_reference_id': data['ref']
            })
            if result in ("CAPTURED", "PROCESSED"):
                _logger.info('KNET payment for tx %s: set as DONE' % (self.reference))
                self._set_transaction_done()
            else:
                msg = 'Received unrecognized response for KNET Payment %s, set as error' % (self.reference)
                _logger.info(msg)
                self._set_transaction_error(msg)
