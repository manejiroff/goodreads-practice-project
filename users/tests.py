from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user

class RegisterUserTestCase(TestCase):
    def test_user_account_is_created(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username':'manejiroff',
                'first_name': 'Shahzod',
                'last_name': 'Omonov',
                'email': 'manejiroff@gmail.com',
                'password': 'somepassword'
            })
        
        user = User.objects.get(username='manejiroff')  
        
        self.assertEqual(user.first_name, 'Shahzod')
        self.assertEqual(user.last_name, 'Omonov')
        self.assertEqual(user.email, 'manejiroff@gmail.com')
        self.assertNotEqual(user.password, 'somepassword')
        self.assertTrue(user.check_password('somepassword'))
        self.assertRedirects(response, reverse('users:login'))

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'email':'manejiroff@gmail.com',
                'last_name':'Omonov',
                'password': 'somepassword'
            }
        )

        user_count = User.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response.context['form'], 'username', 'This field is required.')
    

    def test_duplicate_username(self):
        User.objects.create_user(
            username='manejiroff',
            first_name='Shahzod',
            last_name='Omonov',
            email='test@gmail.com',
            password='somepas'
        )

        response = self.client.post(
            reverse('users:register'),
            data={
                'username':'manejiroff',
                'first_name': 'ziyobek',
                'last_name': 'Omonov',
                'email': 'ziyobek@gmail.com',
                'password': 'somepas'
            }
        )

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'username', 'This username is already taken')

    def test_dublicate_email(self):
        User.objects.create_user(
            username='zikha',
            first_name='ziyobek',
            last_name='hasanov',
            email='manejirof@gmail.com',
            password='somepas'
        )
        response = self.client.post(
            reverse('users:register'),
            data={
                'username':'manejiroff',
                'first_name': 'Shahzod',
                'last_name': 'Omonov',
                'email': 'manejirof@gmail.com',
                'password': 'somepas'
            }
        )

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'email', 'This email is already registered')

    
class LoginUserTestCase(TestCase):
    def test_login_success(self):
        db_user = User.objects.create_user(username='manejiroff')
        db_user.set_password(raw_password='somepass')
        db_user.save()

        self.client.post(
            reverse('users:login'),
            data={
                'username': 'manejiroff',
                'password': 'somepass'
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_login_error_password_or_username(self):
        db_user = User.objects.create_user(username='manejiroff')
        db_user.set_password(raw_password='somepass')
        db_user.save()

        self.client.post(
            reverse('users:login'),
            data={
                'username': 'manejirof',
                'password': 'somepass'
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)
        
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'manejiroff',
                'password': 'somepas'
            }
        )
        
        user = get_user(self.client)
        
        self.assertFalse(user.is_authenticated)

        