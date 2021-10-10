from random import randint, seed
from datetime import datetime
from loader import MailLoader as Mail


class VCode:
    def __init__(self):
        self.time = datetime.now().timestamp()
        seed(self.time)
        self.code = randint(100000, 999999)
        self.verified = False


class Verify:
    email_codes = dict()
    size = 0

    @classmethod
    async def add_code(cls, email):
        code = VCode()
        cls.email_codes[email] = code
        cls.size += 1
        await Mail.sender.send(email, 'Подтверждение почты.', f"Ваш код подтверждения: {code.code}")
        if cls.size > 50:
            cls.__clear_old()

    @classmethod
    async def is_verified_email(cls, email):
        return email in cls.email_codes and cls.email_codes[email].verified is True

    @classmethod
    async def verification(cls, email, code):
        try:
            if cls.email_codes[email].code == code:
                time = datetime.now().timestamp()
                if (time - cls.email_codes[email].time) > 60 * 5:
                    del cls.email_codes[email]
                    raise Exception('Время действия кода истекло!')
                else:
                    cls.email_codes[email].verified = True
                    return True
            else:
                return False
        except KeyError:
            return False

    @classmethod
    def __clear_old(cls):
        time = datetime.now().timestamp()
        for email in cls.email_codes:
            if cls.email_codes[email].time - time > 60 * 15:
                del cls.email_codes[email]
