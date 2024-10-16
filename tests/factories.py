import factory

from fast_zero.models import User
from fast_zero.schemas import TodoSchema


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user_teste_{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}123')


class TodoSchemaFactory(factory.Factory):
    class Meta:
        model = TodoSchema

    title = factory.Sequence(lambda n: f'todo_test_{n}')
    description = factory.LazyAttribute(
        lambda obj: f'Description of {obj.title}'
    )
    state = 'draft'
