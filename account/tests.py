from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from .models import User
from .views import RegistrationView, LoginView, ForgotPasswordView, ChangePasswordView, LogoutView

# Create your tests here.


class UserTest(APITestCase):
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email = 'pimp@gmail.com',
            password = 'pimp',
            is_active = True
        )

    def test_register(self):
        data = {
            'email':'new_user@gmail.com',
            'password': '5432',
            'password_confirm':'5432',
            'name': 'test_name',
            'last_name': 'test_last_name'
        }
        request = self.factory.post('register/', data, format='json')
        view = RegistrationView.as_view()
        response = view(request)
        assert response.status_code == 201
        assert User.objects.filter(email = data['email']).exists()

    def test_login(self):
        data = {
            'email': 'pimp@gmail.com',
            'password': 'pimp'
        }
        request = self.factory.post('login/', data, format = 'json')
        view = LoginView.as_view()
        response = view(request)
        assert response.status_code == 200
        assert 'token' in response.data
        
    def test_change_password(self):
        data = {
            'old_password':'pimp',
            'new_password': '1234',
            'new_password_confirm': '1234'
        }
        request = self.factory.post('change_password/', data, format='json')
        force_authenticate(request, user=self.user)
        view= ChangePasswordView.as_view()
        response = view(request)
        assert response.status_code == 200

    def test_forgot_password(self):
        data = {
            'email':'pimp@gmail.com'
        }
        request = self.factory.post('pass_forgot/', data, format='json')
        view =ForgotPasswordView.as_view()
        response = view(request)
        assert response.status_code == 200
    
    def test_logout(self):
        request = self.factory.post('logout/')
        force_authenticate(request, user=self.user)
        view = LogoutView.as_view()
        response = view(request)
        assert response.status_code == 200
    



