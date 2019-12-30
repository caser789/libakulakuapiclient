from lib_api_client.client import PaymentClient
from lib_api_client.utils import send_third_party_request
from lib_api_client.session_pool import SessionPool

from urlparse import urljoin
import json
import base64
import hashlib


class AkulakuClient(PaymentClient):

    def __init__(self, host, app_id, secret_key, channel_name='Akulaku',
                 timeout=20):
        super(AkulakuClient, self).__init__(channel_name, timeout)
        self.session_pool = SessionPool(
            third_party_urls=[host]
        )
        self.host = host
        self.app_id = app_id
        self.secret_key = secret_key

    def _request(self, path, data):
        endpoint = urljoin(self.host, path)
        return send_third_party_request(
            endpoint,
            data,
            channel_name=self.channel_name,
            request_session=self.session_pool,
        )

    def _sign(self, word):
        content = '%s%s%s' % (self.app_id, self.secret_key, word)
        hash_str = hashlib.sha512(content.encode('utf-8')).digest()
        signature = base64.urlsafe_b64encode(hash_str)
        return signature

    def generate_order(self, ref_no, amount, user_info, callback,
                       item_details=None, item_virtual_details=None):
        data = {
            'appId': self.app_id,
            'refNo': ref_no,
            'totalPrice': amount,  # TODO
            'userAccount': user_info['user_id'],
            'receiverName': user_info['user_name'],
            'receiverPhone': user_info['user_phone'],
            'province': user_info['province'],
            'city': user_info['city'],
            'street': user_info['street'],
            'postcode': user_info['postal_code'],
            'details': json.dumps(item_details) if item_details else '',
            'virtualDetails': (
                json.dumps(item_virtual_details)
                if item_virtual_details else ''
            ),
            'extraInfo': '',
            'callbackPageUrl': callback,
        }
        data['sign'] = self._sign(u''.join((
            data['refNo'],
            str(data['totalPrice']),
            data['userAccount'],
            data['receiverName'],
            data['receiverPhone'],
            data['province'],
            data['city'],
            data['street'],
            data['postcode'],
            data['callbackPageUrl'],
            data['details'],
            data['virtualDetails'],
            data['extraInfo'],
        )))
        path = 'api/json/public/openpay/new.do'
        return self._request(path, data)
