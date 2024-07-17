# funciones extras para la aplicacion Users

import random
import string

def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    codigo = ''.join(random.choice(chars) for _ in range(size))
    print("=================",codigo)
    return codigo