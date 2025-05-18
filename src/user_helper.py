from faker import Faker

faker = Faker()

def random_email():
    return f"user_{faker.pystr(min_chars=8, max_chars=12)}@example.com"