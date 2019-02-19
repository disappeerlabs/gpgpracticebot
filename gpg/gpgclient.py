"""
gpgclient.py

Module for GPGClient class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

from gpg import keyring
from gpg import keyfinder
from gpg import encrypter
from gpg import decrypter
from gpg import signer
from gpg import verifier


class GPGClient:

    def __init__(self, key_dir):
        self.key_dir = key_dir
        self.key_ring = keyring.KeyRing(self.key_dir)
        self.key_finder = keyfinder.KeyFinder(self.key_ring)

    def set(self, new_key_dir):
        self.key_dir = new_key_dir
        self.key_ring.set(new_key_dir)

    def encrypt(self, plaintext, keyid):
        fingerprint = self.key_finder.get_fingerprint_by_keyid(keyid)
        if fingerprint is None:
            return None
        else:
            agent = encrypter.Encrypter(self.key_dir)
            result = agent.execute(plaintext, fingerprint)
            return result

    def decrypt(self, ciphertext, passphrase):
        agent = decrypter.Decrypter(self.key_dir)
        result = agent.execute(ciphertext, passphrase)
        return result

    def export_key(self, keyid):
        result = self.key_ring.export_key(keyid)
        return result

    def import_key(self, pub_key):
        result = self.key_ring.import_key(pub_key)
        return result

    def sign(self, message, keyid, passphrase, detach=False):
        agent = signer.Signer(self.key_dir)
        result = agent.execute(message, keyid, passphrase, detach=detach)
        return result

    def verify(self, message):
        agent = verifier.Verifier(self.key_dir)
        result = agent.execute(message)
        return result
