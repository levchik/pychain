"""
   ___        ___         _     _____    __
  / _ \/\_/\ / __\ /\  /\/_\    \_   \/\ \ \
 / /_)/\_ _// /   / /_/ //_\\    / /\/  \/ /
/ ___/  / \/ /___/ __  /  _  \/\/ /_/ /\  /
\/      \_/\____/\/ /_/\_/ \_/\____/\_\ \/


"""

__title__ = 'pychain'
__version__ = '0.1'
__build__ = 0x0001
__author__ = 'Lev Rubel'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2014 Lev Rubel'

import json
import requests

from exceptions import *

CURRENT_API_VERSION = 'v1'


class ChainAPI(object):
    ALLOWED_BLOCKCHAINS = ['bitcoin', 'testnet3']

    def __init__(self, api_key_id, api_key_secret, blockchain='bitcoin'):
        """
        The Chain API supports the following block chains:
            - Bitcoin Mainnet: https://api.chain.com/<version>/bitcoin
            - Bitcoin Testnet3: https://api.chain.com/<version>/testnet3
        """
        if blockchain not in self.ALLOWED_BLOCKCHAINS:
            raise NotSupportedBlockchain
        self.blockchain = blockchain
        self.session = requests.Session()
        self.session.auth = (api_key_id, api_key_secret)
        self.base_url = 'https://api.chain.com/{}/{}'
        self.api_endpoint = self.base_url.format(CURRENT_API_VERSION, self.blockchain)

    def get(self, url, **params):
        return self.session.get('{}/{}'.format(self.api_endpoint, url), params=params)

    def put(self, url, **params):
        return self.session.put('{}/{}'.format(self.api_endpoint, url), params=params)

    def get_addresses(self, addresses, many=False, end_url='', **params):
        if len(addresses) > 200:
            raise TooManyAddresses
        if not many:
            addresses = [addresses]
        base_url = 'addresses/{}'.format(','.join(addresses))
        response = self.get('{}{}'.format(base_url, end_url), **params)
        if response.status_code == requests.codes.bad_request:
            raise NotValidAddress
        return response.json()

    def addresses(self, addresses, many=False):
        return self.get_addresses(addresses, many)

    def transactions(self, addresses, many=False, limit=50):
        if limit > 500:
            raise MaxTransactionsNumberExceeded
        return self.get_addresses(addresses, many, '/transactions', limit=limit)

    def unspents(self, addresses, many=False):
        return self.get_addresses(addresses, many, '/unspents')

    def address_op_returns(self, address):
        return self.get_addresses(address, False, '/op-returns')

    def get_transactions(self, transaction_hash, end_url=''):
        base_url = 'transactions/{}'.format(transaction_hash)
        response = self.get('{}{}'.format(base_url, end_url))
        if response.status_code == requests.codes.bad_request:
            raise TransactionNotFound
        return response.json()

    def transaction(self, transaction_hash):
        return self.get_transactions(transaction_hash)

    def transaction_op_returns(self, transaction_hash):
        response = self.get_transactions(transaction_hash, '/op-return')
        if response.get('message', '') == 'Transaction does not contain OP_RETURN.':
            return {}
        return response

    def send_transaction(self, transaction_hex):
        response = self.put('transactions', hex=transaction_hex)
        if response.status_code == requests.codes.bad_request:
            raise TransactionRejected
        return response.json().get('hash', '')

    def get_block(self, param, end_url=''):
        base_url = 'blocks/{}'.format(param)
        response = self.get('{}{}'.format(base_url, end_url))
        if response.status_code == requests.codes.bad_request:
            raise BlockNotFound
        return response.json()

    def block_by_hash(self, block_hash):
        return self.get_block(block_hash)

    def block_by_height(self, block_height):
        return self.get_block(block_height)

    def latest_block(self):
        return self.get_block('latest')

    def block_op_returns_by_hash(self, block_hash):
        return self.get_block(block_hash, '/op-returns')

    def block_op_returns_by_height(self, block_height):
        return self.get_block(block_height, '/op-returns')

    def get_webhook(self, webhook_id=None, end_url=''):
        url = self.base_url.format(CURRENT_API_VERSION, 'webhooks')
        if end_url:
            url = '{}/{}{}'.format(url, webhook_id, end_url)
        response = self.session.get(url)
        if response.json().get('message', '') == 'Unable to find webhook.':
            raise WebhookNotFound
        return response.json()

    def post_webhook(self, webhook_id=None, end_url='', data='{}'):
        base_url = 'webhooks'
        if webhook_id:
            base_url = '{}/{}'.format(base_url, webhook_id)
        url = '{}{}'.format(base_url, end_url)
        response = self.session.post(self.base_url.format(CURRENT_API_VERSION, url), data=data)
        if response.status_code == requests.codes.bad_request:
            raise ServerVerificationFailed
        if response.json().get('message', '') == 'Unable to find webhook.':
            raise WebhookNotFound
        return response.json()

    def put_webhook(self, webhook_id, data='{}'):
        base_url = '{}/{}'.format('webhooks', webhook_id)
        response = self.session.put(self.base_url.format(CURRENT_API_VERSION, base_url), data=data)
        if response.status_code == requests.codes.bad_request:
            raise ServerVerificationFailed
        if response.json().get('message', '') == 'Unable to find webhook.':
            raise WebhookNotFound
        if response.json().get('message', '') == 'Invalid Webhook event.':
            raise InvalidWebhookEvent
        return response.json()

    def delete_webhook(self, webhook_id, end_url=''):
        base_url = '{}/{}'.format('webhooks', webhook_id)
        url = '{}{}'.format(base_url, end_url)
        response = self.session.delete(self.base_url.format(CURRENT_API_VERSION, url))
        if response.json().get('message', '') == 'Unable to find webhook.':
            raise WebhookNotFound
        return response.json()

    def create_webhook(self, url, webhook_id=None):
        params = {'url': url}
        if webhook_id:
            params.update({'id': webhook_id})
        return self.post_webhook(data=json.dumps(params))

    def list_webhooks(self):
        return self.get_webhook()

    def update_webhook(self, webhook_id, url):
        params = {'url': url}
        return self.put_webhook(webhook_id, data=json.dumps(params))

    def remove_webhook(self, webhook_id):
        return self.delete_webhook(webhook_id)

    def create_webhook_event(self, webhook_id, event, blockchain, address, confirmations=None):
        if blockchain not in self.ALLOWED_BLOCKCHAINS:
            raise NotSupportedBlockchain
        if confirmations > 10 or confirmations < 0:
            raise InvalidWebhookConfirmationCount
        params = {'event': event, 'blockchain': blockchain, 'address': address}
        if confirmations:
            params.update({'confirmations': confirmations})
        return self.post_webhook(webhook_id, '/events', json.dumps(params))

    def list_webhook_events(self, webhook_id):
        return self.get_webhook(webhook_id, '/events')

    def delete_webhook_event(self, webhook_id, event, address):
        url = '/events/{}/{}'.format(event, address)
        return self.delete_webhook(webhook_id, url)
