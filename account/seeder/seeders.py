from .factories.user_factory import UserFactory


def user_seeder():
    UserFactory.create_batch(10)
