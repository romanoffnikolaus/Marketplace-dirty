from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from .views import StuffViewSet, FavoritesListView, CartView
from .models import Stuffs, Comments, Category, Favorites, Cart
from account.models import User
from django.core.files import File
from collections import OrderedDict

# Create your tests here.


class StuffsTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.category = Category.objects.create(title='cat1')
        user = User.objects.create_user(
            email ='test@gmail.com',
            password = '1234',
            is_active = True,
            name = 'test_name',
            last_name = 'test_last_name'
        )
        img = File(open('media/stuffs_image/2cc4f20786812d864cef0571e24c1cf6_PzGHCSZ.jpg', 'rb'))
        stuffs = [
        Stuffs(seller=user, descriptinon = 'stuff', title='stuff1', image = img, category = self.category, slug=1, price = 100, quantity = 1),
        Stuffs(seller=user, descriptinon = 'stuff2', title='stuff2', image = img, category = self.category, slug=2, price = 100, quantity = 1),
        Stuffs(seller=user, descriptinon = 'stuff3', title='stuff3', image = img, category = self.category, slug=3, price = 100, quantity = 1)
        ]
        Stuffs.objects.bulk_create(stuffs)

    def test_list(self):
        request = self.factory.get('stuffs/')
        view = StuffViewSet.as_view({'get':'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        assert type(response.data) == OrderedDict

    def test_retrieve(self):
        slug = Stuffs.objects.all()[0].slug
        request = self.factory.get(f'stuffs/{slug}')
        view = StuffViewSet.as_view({'get':'retrieve'})
        response = view(request, pk=slug)
        assert response.status_code == 200

    def test_create(self):
        user = User.objects.all()[0]
        data = {
            'descriptinon': 'Новый классный продукт, реализующий весь людской потенциал',
            'title': 'Чудо-нож',
            'category': 'cat1',
            'price':800,
            'quantity':1,
            'seller': 'test@gmail.com'
        }
        request = self.factory.post('stuffs/', data, format='json')
        force_authenticate(request, user=user)
        view = StuffViewSet.as_view({'post':'create'})
        response = view(request)
        assert response.status_code == 201
        assert response.data['title'] == data['title']
    
    def test_add_to_cart(self):
        user = User.objects.all()[0]
        slug = Stuffs.objects.all()[0].slug
        data = {
            'quantity':1,
            }
        request = self.factory.post(f'stuffs/{slug}/add_to_cart', data, format='json')
        force_authenticate(request, user=user)
        view = StuffViewSet.as_view(actions={'post':'add_to_cart'})
        response = view(request, pk = slug)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        user = User.objects.all()[0]
        print(user)
        slug = Stuffs.objects.all()[0].slug
        request = self.factory.delete(f'stuffs/{slug}')
        force_authenticate(request, user=user)
        view = StuffViewSet.as_view({'delete':'destroy'})
        response = view(request, pk=slug)
        assert response.status_code == 204

    def test_update(self):
        user = User.objects.all()[0]
        slug = Stuffs.objects.all()[0].slug
        data = {
            'description': 'Самая нужная вещь',
            'title': 'Балдежный сервилат',
            'price':1500,
            'quantity': 1500
        }
        request = self.factory.patch(f'stuffs/{slug}',data,format='json')
        force_authenticate(request, user=user)
        view = StuffViewSet.as_view({'patch':'partial_update'})
        response = view(request, pk=slug)
        assert response.status_code == 200
        assert response.data['title'] == data['title']
    
    def test_comments(self):
        slug = Stuffs.objects.all()[0].slug
        request = self.factory.get(f'stuffs/{slug}/comments')
        view = StuffViewSet.as_view({'get':'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        assert type(response.data) == OrderedDict
    
    def test_patch_rating(self):
        user = User.objects.all()[0]
        slug = Stuffs.objects.all()[0].slug
        from random import randint
        data = {
            'rating': randint(1, 10)
        }
        request = self.factory.patch(f'stuffs/{slug}/rating/',data,format='json')
        force_authenticate(request, user=user)
        view = StuffViewSet.as_view({'patch':'partial_update'})
        response = view(request, pk=slug)
        assert response.status_code == 200

    def test_favorite(self):
        user = User.objects.all()[0]
        slug = Stuffs.objects.all()[0].slug
        request = self.factory.post(f'stuffs/{slug}/favorite/', format='json')
        force_authenticate(request, user=user)
        view = StuffViewSet.as_view(actions={'post':'favorite'})
        response = view(request, pk = slug)
        self.assertEqual(response.status_code, 200)

    def test_like(self):
        user = User.objects.all()[0]
        slug = Stuffs.objects.all()[0].slug
        request = self.factory.post(f'stuffs/{slug}/like/', format='json')
        force_authenticate(request, user=user)
        view = StuffViewSet.as_view(actions={'post':'like'})
        response = view(request, pk = slug)
        self.assertEqual(response.status_code, 200)

    def test_post_rating(self):
        user = User.objects.all()[0]
        slug = Stuffs.objects.all()[0].slug
        from random import randint
        data = {
            'rating': randint(1, 10)
        }
        request = self.factory.post(f'stuffs/{slug}/rating/', data, format='json')
        force_authenticate(request, user=user)
        view = StuffViewSet.as_view(actions={'post':'rating'})
        response = view(request, pk = slug)
        self.assertEqual(response.data, 'рейтинг сохранен')
        self.assertEqual(response.status_code, 200)
        