from django.test import TestCase

from users.models import UserProfile


class UserCreateTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(
            username='Test',
            first_name='Test 1',
            last_name='prueba test',
            email='testuser@test.com',
            id_rol='1',
            password='123456'
        )
        print('Primer Usuario: ', self.user)

    def test_user_creation(self):
        assert self.user.username == 'Test'
        assert self.user.first_name == 'Test 1'
        assert self.user.last_name == 'prueba test'
        assert self.user.email == 'testuser@test.com'
        assert self.user.id_rol == '1'
