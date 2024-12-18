import random
import string

LOGIN_INFO = {
    'admin': {
      "email": "admin@gmail.com",
      "password": "Admin12345678#"
    },
    'bao': {
      "email": "n.bao25702@gmail.com",
      "password": "P@ssword1"
    },
    'khang': {
      "email": "khangtuhuu@gmail.com",
      "password": "Aa123456789!"
    }
}

def salt(size=15, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def randomNumber():
    return random.randrange(1, 51)

def randomDateUnit():
    return random.choice(["DAY", "MONTH", "YEAR"])