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
        model = "core.User"

    email = factory.LazyFunction(email)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.LazyFunction(lambda: 
        f"{fake.user_name()}.{fake.random_int(1000, 9999)}"
    )


# import faker

# fake = faker.Faker()

# class BookFactory(DjangoModelFactory):
#     class Meta:
#         model = Book

#     title = factory.LazyAttribute(lambda x: fake.sentence(nb_words=4))
#     author = factory.LazyAttribute(lambda x: fake.name())
#     publication_date = factory.LazyAttribute(lambda x: fake.date_between(start_date='-30y', end_date='today'))


# class SubcategoryFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = "api.Subcategory"

#     category = factory.SubFactory(CategoryFactory)
#     description = factory.Faker("sentence"
