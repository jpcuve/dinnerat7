import json
from collections import namedtuple
from typing import Dict, Generator, List

import requests
from flask import Flask

StripeList = namedtuple('StripeList', ['data', 'has_more', 'url'])
StripeCustomer = namedtuple('StripeCustomer', ['id', 'name', 'email'])


def decode(o: Dict):
    t = o.get('object')
    if t == 'customer':
        return StripeCustomer(id=o['id'], name=o['name'], email=o['email'])
    if t == 'list':
        return StripeList(data=[e for e in o['data']], has_more=o['has_more'], url=o['url'])
    return o


class StripeClient:
    def __init__(self, app: Flask = None):
        self.base_url = None
        self.secret_key = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.base_url = app.config['STRIPE_URL']
        self.secret_key = app.config['STRIPE_KEY']

    def __enter__(self):
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {self.secret_key}', 'Accept': 'application/json'})
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()

    def _batch(self, stripe_list: StripeList):
        while True:
            last_object = stripe_list.data[-1]
            last_id = last_object.id  # or subscript?
            yield stripe_list.data
            if not stripe_list.has_more:
                break
            res = self.session.get(f'{self.base_url}{stripe_list.url}?starting_after={last_id}')
            if not res.ok:
                raise ValueError
            stripe_list = json.loads(res.text, object_hook=decode)

    def find_customers(self) -> Generator[List[StripeCustomer], None, None]:
        res = self.session.get(f'{self.base_url}/v1/customers')
        if not res.ok:
            raise ValueError
        return self._batch(json.loads(res.text, object_hook=decode))


stripe = StripeClient()
