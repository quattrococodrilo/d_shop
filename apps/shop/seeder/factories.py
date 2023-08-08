import factory
import faker
from factory.django import DjangoModelFactory


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = "shop.Category"

    name = factory.Faker("word")
    slug = factory.Faker("slug")


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = "shop.Product"

    category = factory.SubFactory(CategoryFactory)
    name = factory.Faker("word")
    slug = factory.Faker("slug")
    description = factory.Faker("paragraph")
    price = factory.Faker("random_int", min=100, max=10000)
    available = factory.Faker("boolean")
