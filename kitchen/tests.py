from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from kitchen.forms import UserRegistrationForm, CookForm, DishTypeForm, DishForm
from kitchen.models import Cook, Dish, DishType


class CookModelTests(TestCase):
    def test_create_cook(self):
        cook = Cook.objects.create(username='chef1', years_of_experience=5)
        self.assertEqual(cook.username, 'chef1')
        self.assertEqual(cook.years_of_experience, 5)

    def test_negative_years_of_experience(self):
        cook = Cook(username='testuser', password='password', years_of_experience=-1)
        with self.assertRaises(ValidationError):
            cook.clean()


class DishTypeModelTests(TestCase):
    def test_create_dish_type(self):
        dish_type = DishType.objects.create(name='Main Course')
        self.assertEqual(dish_type.name, 'Main Course')

    def test_dish_type_name_required(self):
        dish_type = DishType(name='')
        with self.assertRaises(ValidationError):
            dish_type.clean()


class DishModelTests(TestCase):
    def setUp(self):
        self.cook = Cook.objects.create(username='chef1', years_of_experience=5)
        self.dish_type = DishType.objects.create(name='Main Course')

    def test_create_dish(self):
        dish = Dish.objects.create(
            name='Pasta',
            description='Delicious pasta dish.',
            price=12.99,
            dish_type=self.dish_type
        )
        dish.cooks.add(self.cook)
        self.assertEqual(dish.name, 'Pasta')
        self.assertEqual(dish.price, 12.99)
        self.assertIn(self.cook, dish.cooks.all())

    def test_negative_price(self):
        dish = Dish(name='Test Dish', description='A dish.', price=-5.00, dish_type=self.dish_type)
        with self.assertRaises(ValidationError):
            dish.clean()


class DishFormTests(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name='Main Course')
        self.cook = Cook.objects.create(username='chef', years_of_experience=5)

    def test_valid_dish_form(self):
        form_data = {
            'name': 'Pizza',
            'description': 'Delicious cheese pizza',
            'price': 9.99,
            'dish_type': self.dish_type.id,
            'cooks': [self.cook.id],
        }
        form = DishForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_negative_price(self):
        form_data = {
            'name': 'Test Dish',
            'description': 'A delicious dish.',
            'price': -5.00,
            'dish_type': self.dish_type.id,
            'cooks': [],
        }
        form = DishForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('__all__', form.errors)

    def test_missing_name(self):
        form_data = {
            'description': 'A delicious dish.',
            'price': 10.00,
            'dish_type': self.dish_type.id,
            'cooks': [],
        }
        form = DishForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)
        self.assertIn('name', form.errors)


class DishTypeFormTests(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name='Main Course')
        self.cook = Cook.objects.create(username='chef', years_of_experience=5)

    def test_valid_dish_form(self):
        form_data = {
            'name': 'Pizza',
            'description': 'Delicious cheese pizza',
            'price': 9.99,
            'dish_type': self.dish_type.id,
            'cooks': [self.cook.id],
        }
        form = DishForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_name_required(self):
        form_data = {
            'name': '',
        }
        form = DishTypeForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)


class CookFormTests(TestCase):
    def test_valid_cook_form(self):
        form_data = {
            'username': 'testcook',
            'password': 'securepassword',
            'years_of_experience': 5,
            'date_joined': '2023-01-01'
        }
        form = CookForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_negative_years_of_experience(self):
        form_data = {
            'username': 'testcook',
            'password': 'securepassword',
            'years_of_experience': -1,
            'date_joined': '2023-01-01'
        }
        form = CookForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)


class UserRegistrationFormTests(TestCase):
    def test_valid_user_registration_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'user@example.com',
            'password': 'securepassword',
            'password_confirm': 'securepassword',
            'years_of_experience': 2
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        form_data = {
            'username': 'newuser',
            'email': 'user@example.com',
            'password': 'securepassword',
            'password_confirm': 'differentpassword',
            'years_of_experience': 2
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)


class DishViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password'
        )
        self.client.login(username='testuser', password='password')
        self.dish_type = DishType.objects.create(name='Main Course')

        self.cook = Cook.objects.create(
            username='chef',
            years_of_experience=5
        )
        self.dish = Dish.objects.create(
            name='Pizza',
            description='Delicious cheese pizza',
            price=9.99,
            dish_type=self.dish_type
        )
        self.dish.cooks.add(self.cook)

    def test_dish_create_view(self):
        response = self.client.post(reverse('kitchen:dish-create'), {
            'name': 'Pasta',
            'description': 'Delicious pasta dish.',
            'price': 12.99,
            'dish_type': self.dish_type.id,
            'cooks': [self.cook.id],
        })

        self.assertEqual(response.status_code, 302)

        self.assertTrue(Dish.objects.filter(name='Pasta').exists())

        if response.status_code != 302:
            form = response.context.get('form')
            if form:
                print("Form errors:", form.errors)
            else:
                print("No form in the response")

    def test_dish_list_view(self):
        response = self.client.get(reverse('kitchen:dish-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kitchen/list_of_dish.html')
        self.assertIn('dishes', response.context)
        self.assertContains(response, 'Pizza')

    def test_dish_update_view(self):
        response = self.client.post(reverse('kitchen:dish-update', args=[self.dish.id]), {
            'name': 'Updated Pizza',
            'description': 'Even better pizza.',
            'price': 10.99,
            'dish_type': self.dish_type.id,
            'cooks': [self.cook.id],
        })
        self.assertEqual(response.status_code, 302)
        self.dish.refresh_from_db()
        self.assertEqual(self.dish.name, 'Updated Pizza')

    def test_dish_delete_view(self):
        response = self.client.post(reverse('kitchen:dish-delete', args=[self.dish.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Dish.objects.count(), 0)

    def test_access_denied_for_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('kitchen:dish-create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/kitchen/dish/create/')

    def test_invalid_dish_form(self):
        response = self.client.post(reverse('kitchen:dish-create'), {
            'name': '',
            'description': 'Tasty dish',
            'price': -10,
            'dish_type': '',
        })

        form = response.context['form']

        self.assertFalse(form.is_valid())

        # Перевірте помилки
        self.assertIn('name', form.errors)
        self.assertIn('dish_type', form.errors)

        self.assertIn('__all__', form.errors)
        self.assertEqual(form.errors['__all__'],
                         ['Price must be greater than or equal to 0', 'Price must be greater than or equal to 0.'])
