from db.filter_sets.users import UsersFilterSet
from db.orm import User
from db.repository.create_update_mixin import CreateUpdateMixin
from db.repository.list_mixin import ListMixin
from db.repository.retrieve_mixin import RetrieveMixin


class UserRepository(
    CreateUpdateMixin[User],
    ListMixin[User, UsersFilterSet],
    RetrieveMixin[User],
):
    model = User
    filter_set = UsersFilterSet

