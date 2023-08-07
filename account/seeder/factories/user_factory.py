from django.contrib.auth.hashers import make_password
import factory
import faker
from factory.django import DjangoModelFactory

fake = faker.Faker()


def email():
    email = fake.email()
    email_split = email.split("@")
    return f"{email_split[0]}.{fake.random_int(1000, 9999)}@{email_split[1]}"


class UserFactory(DjangoModelFactory):
    class Meta:
        model = "account.User"

    email = factory.LazyFunction(email)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.LazyFunction(lambda: 
        f"{fake.user_name()}.{fake.random_int(1000, 9999)}"
    )
    password = make_password("password")
