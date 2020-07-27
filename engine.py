from Crypto.Cipher import AES
from os import urandom
from random import random


class Encryptor:
    def pad(s):
        return s + ((16 - len(s) % 16) * '`')

    def __init__(self):
        self.key = urandom(32)
        self.cipher = AES.new(self.key)

    def encrypt(self, text):
        return self.cipher.encrypt(Encryptor.pad(text))

    def decrypt(self, ciphertext):
        decipher =  self.cipher.decrypt(ciphertext).decode('utf-8')
        padsize = decipher.count('`')
        return decipher[:(len(decipher)-padsize)]

class ChatStack:

    def __init__(self):
        self.stack = []

    def push(self, data):
        msg_encryptor = Encryptor()
        self.stack.insert(0, (msg_encryptor.encrypt(str(data)), msg_encryptor))

    def decrypt_top_stack(self):
        top_encryptor = self.stack[0][1]
        top_cipher = self.stack[0][0]
        return top_encryptor.decrypt(top_cipher)
