# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

import logging
import pprint
import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class KNETController(http.Controller):
    _response_url = '/payment/knet/response'

    @http.route(_response_url, type='http', auth='public', csrf=False, save_session=False)
    def knet_form_feedback(self, **post):
        _logger.info('KNET: entering form_feedback with post data %s', pprint.pformat(post))
        request.env['payment.transaction'].sudo().form_feedback(post, 'knet')
        return werkzeug.utils.redirect('/payment/process')
