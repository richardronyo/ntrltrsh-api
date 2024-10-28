from AESPython import *

#These are just some examples for how to hash and encrypt/decrypt data
#Uncomment them as you need them

"""
#Hashing Example:
input_password = 'mysecretpassword'
salt, hash = hash_password(input_password)
#User password and input password match
user_password = 'mysecretpassword'
match = verify_password(user_password, salt, hash)
print(match)
#User password and input password do not match
user_password = 'Idontknowthesecret'
match = verify_password(user_password, salt, hash)
print(match)
"""

#Elsaadany said that security should be considered a nice to have, so implement this only if time permits
"""
#Encryption/Decryption Example:
key = get_random_bytes(32)  # AES-256 key
                            #This will need to be a fixed key to simplify our implementation.
                            #OR implement some kind of simple key management / generation system, but idk how
data = 'user@example.com'
encrypted_data, iv = encrypt_data(key, data)
#store in database
#get from database
decrypted_data = decrypt_data(key, encrypted_data, iv)
print(f'Decrypted data: {decrypted_data}')

data2 = 'ILoveMyCat23876'
encrypted_data, iv = encrypt_data(key, data2)
#store these in database

#get data and iv from database
decrypted_data = decrypt_data(key, encrypted_data, iv)
print(f'Decrypted data: {decrypted_data}')
"""

"""
#Test password concatenation and split functions
#Put a password into the database:
user = {"PASSWORD": "ArtificialRecycling395"}
user = update_password_field(user)
print(user["PASSWORD"]) #This is the password field in the database, stored in hex in format [salt]:[password]

password = "ArtificialRecycling395" #This is the password the user enters
#Now, lets break the salt and password hash apart
database_salt, database_password_hash = split_salt_and_password(user["PASSWORD"])
print(database_salt)
print(database_password_hash)
#Now, salt the user input password with the database salt
user_password_hash = hash_password_with_salt(database_salt, password)
print(user_password_hash)

#Verify password
if (database_password_hash == user_password_hash):
    # User authenticated successfully
    print("Success!")
else:
    print("Failure")
"""