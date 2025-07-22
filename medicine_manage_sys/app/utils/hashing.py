from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """加密明文密码"""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """校验密码"""
    return pwd_context.verify(plain_password, hashed_password)


# if __name__ == '__main__':
#     print(get_password_hash('123456'))
#     verify_password('123456', '$2b$12$qHicWXcNWRZylYOIOX00iOlB1EhYQ8j.BuK07U3aI4HuVlWLM3Yre') == False:


