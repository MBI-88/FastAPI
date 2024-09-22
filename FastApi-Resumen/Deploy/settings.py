from pydantic import BaseSettings

class Settings(BaseSettings):
    debug: bool = True
    enviroment: str
    database_url: str 
    
    # Usando .env
    
    class Config:
        env_file = '.env'
    