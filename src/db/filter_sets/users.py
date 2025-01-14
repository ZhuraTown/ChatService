from sqlalchemy_filterset import BaseFilterSet, SearchFilter, InFilter

from db.orm import User


class UsersFilterSet(BaseFilterSet):
    search = SearchFilter(User.name, User.email)
    email__in = InFilter(User.email)
    name__in = InFilter(User.name)
    id__in = InFilter(User.id)