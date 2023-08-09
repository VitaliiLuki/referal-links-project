import random

CHARS = ('+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyz'
         'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
INV_CODE_LENGHT = 6


def generate_random_inv_code():
    """
    Generates random code with lengh equal to INV_CODE_LENGHT.
    """
    inv_code = ''
    for i in range(INV_CODE_LENGHT):
        inv_code += random.choice(CHARS)
    return inv_code


def generate_auth_code():
    """Generates 4-digit code."""
    return str(random.randint(1000, 9999))
