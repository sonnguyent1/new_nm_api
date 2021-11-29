import hashlib
from django.contrib.auth.hashers import MD5PasswordHasher

from django.utils.encoding import force_bytes

class NewNMMD5PasswordHasher(MD5PasswordHasher):

    def encode(self, password, salt):
            assert password is not None
            assert salt and '$' not in salt
            print('reached here !!!!!!!!!!!')
            hash = hashlib.md5(force_bytes(password + salt)).hexdigest()
            return "%s$%s$%s" % (self.algorithm, salt, hash)