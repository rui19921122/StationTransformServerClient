from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.request import Request

from article.models import Article
from .models import Menu, MenuPickle
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


# Create your tests here.
class TestGetMenus(APITestCase):
    def setUp(self):
        user = User.objects.last()
        if user:
            pass
        else:
            User.objects.create_user(username='test1',
                                     password='111111'
                                     )
            user = User.objects.last()
            self.user = user
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
        Menu.objects.create(
            name='测试子目录2',
            owner=user,
            parent=Menu.objects.get(name='测试子目录')
        )
        Menu.objects.create(
            name='测试子目录3',
            owner=user,
            parent=Menu.objects.get(name='测试子目录2')
        )
        Menu.objects.create(
            name='测试子目录4',
            owner=user,
            parent=Menu.objects.get(name='测试子目录3')
        )
        self.test_article = Article.objects.create(
            name='测试文章',
            create_person=user,
            content='测试内容',
            menu_id=Menu.objects.get(name='测试目录').pk
        )

    def test_list_menu(self):
        url = reverse('menu-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data.get('items')), 7,response.data)
        self.assertListEqual(response.data.get('sort'),
                             [
                                 {'id': Menu.objects.get(name='测试目录').id, 'children': [
                                     {'id': Menu.objects.get(name='测试子目录').id, 'children': [
                                         {'id': Menu.objects.get(name='测试子目录2').id, 'children': [
                                             {'id': Menu.objects.get(name='测试子目录3').id, 'children': [
                                                 {'id': Menu.objects.get(name='测试子目录4').id, 'children': []}
                                             ]}
                                         ]}
                                     ]}
                                 ]},
                                 {'id': Menu.objects.get(name='测试目录1').id, 'children': []},
                                 {'id': Menu.objects.get(name='测试目录2').id, 'children': []},
                             ]
                             )

    def test_add_root_menu(self):
        user = User.objects.create_superuser(
            username='superuser',
            password='qq5234771735',
            email='1@qq.com'
        )
        self.client.force_login(user)
        url = reverse('menu-list')
        response = self.client.post(url, data={'name': '测试的添加根'})
        self.assertEqual(response.status_code, 201, response.data)

    def test_delete_menu(self):
        name = Menu.objects.get(name='测试目录')
        url = reverse('menu-detail', args=(name.id,))
        self.client.force_login(name.owner)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT, res.data)
        self.assertEqual(False, Menu.objects.filter(name='测试目录').exists())

    def test_delete_menu_with_other_people(self):
        name = Menu.objects.get(name='测试目录')
        url = reverse('menu-detail', args=(name.id,))
        user = User.objects.create_user(username='1', password='111111')
        self.client.force_login(user)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN, res.data)
        self.assertEqual(True, Menu.objects.filter(name='测试目录').exists())

    def test_delete_no_exist_menu(self):
        count = Menu.objects.all().count()
        url = reverse('menu-detail', args=(count + 1,))
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND, res.data)

    def test_add_child_menu(self):
        menu = Menu.objects.get(name='测试目录')
        url = reverse('menu-child', args=[menu.id])
        self.client.force_login(menu.owner)
        res = self.client.post(url, {'name': '测试添加子目录'})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED,
                         res.data)
        self.assertEqual(
            Menu.objects.get(name='测试添加子目录').parent_id,
            menu.id
        )

    def test_add_administrator(self):
        menu = Menu.objects.get(name='测试目录')
        url = reverse('menu-administrator', args=[menu.id])
        self.client.force_login(menu.owner)
        res = self.client.post(url, data={'pk': User.objects.first().id})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED, res.data)

    def test_get_administrator(self):
        menu = Menu.objects.get(name='测试目录')
        menu.administrators.add(menu.owner)
        url = reverse('menu-administrator', args=[menu.id])
        self.client.force_login(menu.owner)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.data)

    def test_remove_administrator(self):
        menu = Menu.objects.get(name='测试目录')
        menu.administrators.add(menu.owner)
        url = reverse('menu-administrator-detail', args=[menu.id, menu.owner.id])
        self.client.force_login(menu.owner)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT, res.data)

    def test_get_menu_articles(self):
        menu = Menu.objects.get(name='测试目录')
        menu.article_set.add(
            self.test_article
        )
        url = reverse('menu-articles', args=[menu.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200, res.data)
        self.assertEqual(res.data[0].get('name'), self.test_article.name)
        self.assertEqual(res.data[0].get('id'), self.test_article.id)
        self.assertEqual(res.data[0].get('content'), self.test_article.content)

    def test_post_articles_with_wrong_person(self):
        self.client.logout()
        menu = Menu.objects.get(name='测试目录')
        data = {
            'name': '新增测试文章',
            'content': 'test_content',
        }
        url = reverse('menu-articles', kwargs={'pk': menu.id})
        res = self.client.post(url,
                               data=data)
        self.assertEqual(res.status_code,
                         status.HTTP_403_FORBIDDEN,
                         res.data)

    def test_post_article_with_true_person(self):
        menu = Menu.objects.get(name='测试目录')
        data = {
            'name': '新增测试文章',
            'content': 'test_content',
        }
        menu.administrators.add(
            self.user
        )
        self.client.force_login(self.user)
        url = reverse('menu-articles', kwargs={'pk': menu.id})
        res = self.client.post(url,
                               data=data)
        self.assertEqual(res.status_code,
                         status.HTTP_201_CREATED)
        self.assertEqual(True,
                         Article.objects.filter(name='新增测试文章').exists())
