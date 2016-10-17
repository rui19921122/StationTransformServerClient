from rest_framework.test import APITestCase
from .models import Menu
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


# Create your tests here.
class TestGetMenus(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username='test',
                                        password='111111'
                                        )
        menus = [
            '测试目录',
            '测试目录1',
            '测试目录2',
        ]
        for menu in menus:
            Menu.objects.create(
                name=menu,
                owner=user,
            )
        Menu.objects.create(
            name='测试子目录',
            owner=user,
            parent=Menu.objects.get(name='测试目录')
        )

    def test_list_menu(self):
        url = reverse('list-menu')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.body.get('items')), 4)
        self.assertEqual(len(response.body.get('sort')),
                         [
                             {'id': 1, 'children': [
                                 {'id': 4, 'children': []}
                             ]},
                             {'id': 2, 'children': []},
                             {'id': 3, 'children': []},
                         ]
                         )
