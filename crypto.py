import bcrypt
from config import load_config

def encriptar_variable(password):
    salt = load_config ('app_config.ini', 'bcrypt_salt')
    
    salt1 = salt.get('salt') 
    salt2 = bytes(salt1.encode('utf-8'))
    print(salt)
    print(salt1)
    print(salt2)
    hashed_password = bcrypt.hashpw(password, salt2)
    return hashed_password


if __name__ == '__main__':
    config = load_config ('app_config.ini', 'bcrypt_salt')
    print(config)
