from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256

#This file includes functions for hashing/checking passwords, encrypting/decrypting info, and converting from string to binary string and back

def string_to_bytes(input_string):
    #This function encodes the string to bytes using UTF-8 encoding
    #Input: input_string: The string to encode to bytes
    #Return: bytes_obj: The bytes object representing our string
    bytes_obj = input_string.encode('utf-8')
    return bytes_obj

def string_from_bytes(bytes_obj):
    #This function decodes the string from bytes using UTF-8 encoding
    #Input: bytes_obj: The bytes object we want to convert to string
    #Return: result_string: the resulting string after decoding
    result_string = bytes_obj.decode('utf-8')
    return result_string

# User sign-up: hash the password
def hash_password(input_password):
    #This function will hash the user entered password for the first time during sign-up
    #Input: input_password: the user entered password
    #Returns: salt: the salt used when encrypting the password (need to store in database)
    #         hash: the hashed password (need to store in database)
    bin_password = string_to_bytes(input_password)
    salt = get_random_bytes(16)
    hash = PBKDF2(bin_password, salt, dkLen=32, count=1000000, hmac_hash_module=SHA256)
    return salt, hash

def hash_password_with_salt(salt, input_password):
    #This function will hash a user entered password with a salt found in the database (needed to compare password with that already in the database)
    #Input: input_password: the user entered password
    #       salt: the salt found in the database
    #Returns: salt: the salt used when encrypting the password (need to store in database)
    #         hash: the hashed password (need to store in database)
    bin_password = string_to_bytes(input_password)
    hash = PBKDF2(bin_password, salt, dkLen=32, count=1000000, hmac_hash_module=SHA256)
    return hash

def update_password_field(user):
    #This function will change the data of the password field of user
    #Input: user dictionary with keys and values from the json file
    #Return: user dictionary with the password value updated
    password = user['PASSWORD']
    salt, hash = hash_password(password)
    user['PASSWORD'] = salt.hex() + ':' + hash.hex() #Store salt and hash as a concatenated string seperated by a :
    #Storing salt and hash as hex values allows us to use a : as a delimiter since it won't appear in the hex
    #However, this means we will have to convert them both back to binary representation when we want to use them again (see split_salt_and_password)
    return user

def split_salt_and_password(password):
    #This function will split the salt from the password in the database
    #Input: password: the string found in the password field in the database
    #Return: salt: The salt in the database in byte form
    #        password_hash: The hash of the password in the database in byte form
    password_parts = password.split(':')
    salt = bytes.fromhex(password_parts[0])
    password_hash = bytes.fromhex(password_parts[1])
    #need to convert these back to bytes before returning
    return salt, password_hash

# User login: verify the password
def verify_password(input_password, stored_salt, stored_hash):
    #This function will verify the user entered password against that in the database
    #Inputs: input_password: the user entered password
    #        stored_salt: the salt needed to hash the user entered password (retrieve from database)
    #        stored_hash: the hashed password in the database
    #Returns: True if passwords match, or false if they don't
    bin_password = string_to_bytes(input_password)
    input_hash = PBKDF2(bin_password, stored_salt, dkLen=32, count=1000000, hmac_hash_module=SHA256)
    if input_hash == stored_hash:
        return True #Password is correct
    else:
        return False #Password is incorrect

# Encrypt data
def encrypt_data(key, data):
    #This function will encrypt non-password user data using AES-256
    #Input: key: the encryption key
    #       data: the data to be encrypted
    #returns: encrypted_data: the encrypted data (store in database)
    #         cipher.iv: the iv for the cipher (needed for decryption) (store in database)
    bytes_data = string_to_bytes(data)
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted_data = cipher.encrypt(pad(bytes_data, AES.block_size))
    return encrypted_data, cipher.iv

# Store 'encrypted_data', 'cipher.iv' in the database

# Decrypt data
def decrypt_data(key, encrypted_data, iv):
    #This function will decrypt non-password data
    #Input: key: the decryption key
    #       encrypted_data: The data to be decrypted
    #       iv: the cipher iv
    #Return: decrypted_data: the decrypted data
    cipher_dec = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher_dec.decrypt(encrypted_data), AES.block_size)
    string_data = string_from_bytes(decrypted_data)

    return string_data