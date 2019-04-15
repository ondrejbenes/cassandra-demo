""" Generates Transactions which can be used during learning. """

import uuid
import random
from typing import List
from dataclasses import dataclass
from collections.abc import Generator


class TransationsGenerator(Generator):

    def __init__(self, users_count=10, receiver_account_numbers=None):
        self._users = []
        self._prepare_users(users_count)

        if not receiver_account_numbers:
            receiver_account_numbers = [
                self._make_account_number() for _ in range(50)
            ]

        self.receiver_account_numbers = receiver_account_numbers

    def send(self, value):
        amount = random.randint(0, 10000)
        sender = random.choice(self._users)
        ip = random.choice(sender.known_ips)
        fingerprint = random.choice(sender.known_browser_fingerprints)
        receiver_account = random.choice(self.receiver_account_numbers)

        return Transaction(sender.account_number, receiver_account, amount, ip,
                           fingerprint)

    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration

    def _prepare_users(self, users_count):
        for _ in range(users_count):
            account_number = self._make_account_number()
            ips = self._make_known_ips()
            fingerprints = self._make_known_browser_fingerprints()

            self._users.append(_User(account_number, ips, fingerprints))

    @staticmethod
    def _make_account_number():
        user_number = str(random.randint(0, 10**9)).zfill(9)
        bank_number = str(random.randint(0, 10**4)).zfill(4)

        return '{}/{}'.format(user_number, bank_number)

    @staticmethod
    def _make_known_ips():
        def make_ip():
            return '.'.join([str(random.randint(0, 255)) for _ in range(4)])

        count = 1 + int(random.random() // 0.3)

        return [make_ip() for _ in range(count)]

    @staticmethod
    def _make_known_browser_fingerprints():
        count = 1 + int(random.random() // 0.3)
        return [str(uuid.uuid4()) for _ in range(count)]


@dataclass
class Transaction():
    sender_account_number: str
    receiver_account_number: str
    amount: float
    sender_ip: str
    sender_browser_fingerprint: str


@dataclass
class _User():
    account_number: str
    known_ips: List[str]
    known_browser_fingerprints: List[str]
