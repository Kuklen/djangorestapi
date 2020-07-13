from rest_framework.test import APITestCase
from django.urls import reverse

"""
doğru veriler ile kayıt işlemi yap
şifre invalid olabilir
kullanıcı adı kullanılmış olabilir
üye girişi yaptıysak o sayfa gözükmemeli
token ile giriş yapıldığında 403 hatası
"""
class UserRegistrationTestCase(APITestCase):
    url = reverse("account:register")
    url_login = reverse("token_obtain_pair")

    def test_user_registration(self):
        """
        Doğru veriler ile kayıt işlemi.
        """
        data = {
            "username": "Ugurtest",
            "password": "alizutuli12"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_user_invalid_password(self):
        """
        invalid password ile kayıt işlemi.
        """
        data = {
            "username": "Ugurtest",
            "password": "1"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_unique_name(self):
        """
        benzersiz isim testi.
        """
        self.test_user_registration()
        data = {
            "username": "Ugurtest",
            "password": "deneme123"
        }
        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    def test_user_authenticated_registration(self):
        """
        session ile giriş yapmış kullanıcı sayfayı görememeli.
        """
        self.test_user_registration()
        self.client.login(username='Ugurtest', password='asdasda123')
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)

    def test_user_authenticated_token_registration(self):
        """
        token ile giriş yapmış kullanıcı sayfayı görememeli.
        """
        self.test_user_registration()
        data = {
            "username": "Ugurtest",
            "password": "deneme123"
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION= 'Bearer ' + token)
        response_2 = self.client.get(self.url)
        self.assertEqual(403, response_2.status_code)



