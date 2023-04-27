# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

import logging

from Cryptodome.Cipher import AES
from werkzeug import urls

from odoo import fields, models, _
from odoo.addons.payment_knet.controllers.main import KNETController
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class PaymentAcquirerBenefitPay(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[("knet", _("KNET"))], ondelete={"knet": "set default"})
    knet_tranportal_id = fields.Char(string="Transportal ID", required_if_provider="knet", groups='base.group_user')
    knet_tranportal_password = fields.Char(string="Transportal Password", required_if_provider="knet", groups='base.group_user')
    knet_terminal_resource_key = fields.Char(string="Terminal Resource Key", required_if_provider="knet", groups='base.group_user')

    def _get_knet_urls(self):
        if self.state == "enabled":
            return "https://www.kpay.com.kw/kpg/PaymentHTTP.htm?"
        else:
            return "https://kpaytest.com.kw/kpg/PaymentHTTP.htm?"

    def encryptAES(self, plain_data):
        raw = self._pad(plain_data.encode("UTF-8"))
        iv = self.knet_terminal_resource_key.encode('UTF-8')
        cipher = AES.new(self.knet_terminal_resource_key.encode('UTF-8'), AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(raw.encode('UTF-8'))
        return encrypted_text.hex()

    def decrypt(self, enc):
        iv = self.knet_terminal_resource_key.encode('UTF-8')
        cipher = AES.new(self.knet_terminal_resource_key.encode('UTF-8'), AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(bytes.fromhex(enc)).decode('UTF-8'))

    def _pad(self, s):
        return s.decode('UTF-8') + (AES.block_size - len(s.decode('UTF-8')) % AES.block_size) * chr(AES.block_size - len(s.decode('UTF-8')) % AES.block_size)

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

    def join_parameters(self, params):
        res = ""
        for k, v in params.items():
            res += f"{k}={v}&"
        return res

    def knet_form_generate_values(self, values):
        base_url = self.get_base_url()
        if values.get('currency') != self.env.ref('base.KWD'):
            raise UserError(_("KNET supports only KWD currency !"))

        raw_str = self.join_parameters({
            "id": self.knet_tranportal_id,
            "password": self.knet_tranportal_password,
            "langid": "AR" if values.get('partner_lang').split("_")[0] == "ar" else "USA",
            "trackid": values.get('reference'),
            "amt": '%.3f' % values.get('amount'),
            "currencycode": "414",
            "action": "1",
            "responseURL": urls.url_join(base_url, KNETController._response_url),
            "errorURL": urls.url_join(base_url, KNETController._response_url)
        })
        enc_str = self.encryptAES(raw_str)
        req_str = self.join_parameters({
            "param": "paymentInit",
            "trandata": enc_str,
            "tranportalId": self.knet_tranportal_id,
            "responseURL": urls.url_join(base_url, KNETController._response_url),
            "errorURL": urls.url_join(base_url, KNETController._response_url),
        })
        values.update({'api_url': self._get_knet_urls() + req_str})
        return values
