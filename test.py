import unittest
import uuid
from lib_akulaku_api_client.client import AkulakuClient


class AkulakuClientTestCase(unittest.TestCase):

    def test_generate_order(self):
        host = 'https://test-id-app.akulaku.com'
        app_id = 73124300
        secret_key = '1mZkWtPpQda5tPoCjN1KXwT3UidigpJTSEcNlzvKnuk'
        client = AkulakuClient(host, app_id, secret_key)

        ref_no = uuid.uuid4().hex
        amount = 100
        user_info = {
            'user_id': '11195355',
            'user_name': 'Mikhael',
            'user_phone': '6289616961490',
            'province': 'BANTEN',
            'city': 'KAB. TANGERANG',
            'street': 'Dasana Indah blok UB 4 no 16 Bojong Nangka',
            'postal_code': '15820',
        }
        callback = ''
        item_details = [
            {
                "skuId": "4812514664",
                "img": "",
                "vendorId": 24940114,
                "qty": 1,
                "skuName": 'HP 14s-cf1051TU (14\\", Celeron-4205U, 4GB, 512GB SSD, Silver)',
                "unitPrice": 4400000,
                "vendorName": "ITPRO Teknologi",
            },
        ]
        res = client.generate_order(ref_no, amount, user_info, callback, item_details=item_details)
        print(res)


if __name__ == '__main__':
    unittest.main()
