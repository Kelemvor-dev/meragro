from django.test import TestCase

from products.models import Category, Product
from users.models import UserProfile


class ProductCreateTestCase(TestCase):
    def setUp(self):

        self.user = UserProfile.objects.create_user(
            id=1,
            username='Test',
            first_name='Test 1',
            last_name='prueba test',
            email='testuser@test.com',
            id_rol='1',
            password='123456'
        )

        self.category = Category.objects.create(
            id=1,
            name='Alimentos'
        )

        self.product = Product.objects.create(
            title='Prueba',
            image='product/1.png',
            content='Esto es un producto de prueba',
            price='15000',
            id_category_id=self.category.id,
            id_user_id=self.user.id
        )

    def test_product_creation(self):
        assert self.product.title == 'Prueba'
        assert self.product.image == 'product/1.png'
        assert self.product.content == 'Esto es un producto de prueba'
        assert self.product.price == '15000'
        assert self.product.id_category_id == 1
        assert self.product.id_user_id == 1
