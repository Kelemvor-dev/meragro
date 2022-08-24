from django.test import TestCase

from users.models import UserProfile


class UserUpdateTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.update_user(
            first_name='Test update',
            last_name='prueba test update',
            email='testuser@test.com',
            id_rol='1'
        )

    def test_user_update(self):
        assert self.user.first_name == 'Test update'
        assert self.user.last_name == 'prueba test update'
        assert self.user.email == 'testuser@test.com'
