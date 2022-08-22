from django.test import TestCase

from users.models import UserProfile


class UserUpdateTestCase(TestCase):
    def setUp(self):
        id = UserProfile.objects.get_user(1)
        self.user = UserProfile.objects.update_user(
            id=id,
            first_name='Test update',
            last_name='prueba test update',
            email='testuser@test.com',
            id_rol='1'
        )
        print('Usuario Actualizado: ', self.user)

    def test_user_update(self):
        assert self.user.first_name == 'Test update'
        assert self.user.last_name == 'prueba test update'
        assert self.user.email == 'testuser@test.com'
