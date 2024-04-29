from api.services.user import UserService
from api.repositories.user import UserRepository

user_repo = UserRepository()
user_service = UserService(user_repo)
def get_user_service():
    return user_service
