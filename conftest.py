import pytest
from django.contrib.auth import get_user_model


@pytest.fixture(autouse=True)
def create_test_users(db):
    """Автоматически создаёт трёх пользователей для всех тестов."""
    User = get_user_model()

    if User.objects.count() == 0:
        User.objects.create_user(
            first_name='firstname1',
            last_name='lastname1',
            username="user1",
            password="password1"
        )
        User.objects.create_user(
            first_name='firstname2',
            last_name='lastname2',
            username="user2",
            password="password2"
        )
        User.objects.create_user(
            first_name='firstname3',
            last_name='lastname3',
            username="user3",
            password="password3"
        )
        print("\n=== Тестовые пользователи созданы ===")
    else:
        print(f"\n=== В базе уже есть {User.objects.count()} пользователей ===")
