from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash class

class HashPassword:
    def create_hash(self, password: str) -> None:
        return pwd_context.hash(password)

    def verify_hash(self,plain_password:str,hashed_password:str) -> bool:
        return pwd_context.verify(plain_password,hashed_password)