import string
import random
import unittest2 as unittest
from obfuscol.obfuscol import obfs_host

class Obfs_host_test(unittest.TestCase):
    def test_Null_Host(self):
        self.assertEqual(obfs_host(''), 'Null')

    def test_host_is_obfuscated(self):
        self.assertNotEqual(obfs_host('test'), 'test')

    def test_encoded_host_has_same_length(self):
        self.assertEqual(len(obfs_host('test')), len('test'))

    def test_domain_not_obfuscated(self):
        self.assertTrue(obfs_host('test.example.com').endswith('.example.com'))

    def test_randomize_chars_has_no_uppercase(self):
        # Since the chars are random, let's use a long hostname to reduce
        # probability of false positives
        charset = string.ascii_uppercase 
        host_string = ''.join(random.choice(charset) for i in range(1000)) 
        self.assertFalse([c for c in obfs_host(host_string) if c.isupper()])

