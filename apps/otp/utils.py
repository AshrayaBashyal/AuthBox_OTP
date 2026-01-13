import pyotp

def generate_otp(secret=None):
    secret = secret or pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=300)
    return secret, totp.now()

def verify_otp(secret, otp):
    totp = pyotp.TOTP(secret, interval=300)
    return totp.verify    
    