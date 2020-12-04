import hashlib
import os

path = 'C:/Users/Adrian/Downloads'
path_obj = open(path,"rb")
file_var = path_obj.read()

hash_val = hashlib.sha512(file_var)
hashed = hash_val.hexdigest()
print(hashed)

