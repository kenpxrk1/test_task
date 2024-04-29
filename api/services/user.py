from typing import List
from api.repositories.user import UserRepository
from api.schemas import UserReadDTO, UserСreateDTO
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository 

    async def create_user(self, request: UserСreateDTO) -> None:
        """
        create_user taking in params a request with UserCreateDTO object, 
        deserialize it into a dict object, hashing password from request 
        and sends new object to database logic.
         
        """
        request_dict = request.model_dump()
        request_dict["password"] = bcrypt_context.hash(request_dict["password"])
        await self.repository.create_user(request_dict)


    async def get_users(self) -> List[UserReadDTO | None]:
        """
        calling a self repository get_users method and returns 
        list of UserReadDTO objects. 
        """
        users = await self.repository.get_users()
        return users 
    
