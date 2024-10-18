import factory
import factory.fuzzy

from fast_zero.models import Todo, TodoState, User
from fast_zero.schemas import TodoSchema, UserSchema


class UserSchemaFactory(factory.Factory):
    class Meta:
        model = UserSchema

    username = factory.Sequence(lambda n: f'user_teste_{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}123')


class UserModelFactory(UserSchemaFactory):
    class Meta:
        model = User


class TodoSchemaFactory(factory.Factory):
    class Meta:
        model = TodoSchema

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)


class TodoModelFactory(TodoSchemaFactory):
    class Meta:
        model = Todo

    user_id = -1
