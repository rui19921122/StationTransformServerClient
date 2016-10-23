from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from menu.models import MenuPickle, Menu
from article.models import Article, File, User


# Create your tests here.

class TestArticle(APITestCase):
    def setUp(self):
        self.super_user = User.objects.create_superuser(
            username='test',
            password='111111',
            email='1@qq.com'
        )
        self.normal_user = User.objects.create_user(
            username='test_user',
            password='111111'
        )
        self.root_menu = Menu.objects.create(
            name='根目录',
            owner=self.super_user
        )
        self.root_menu.administrators.add(self.normal_user)
        self.test_article = Article.objects.create(
            name='测试文章',
            create_person=self.normal_user,
            content='测试内容',
            menu=self.root_menu
        )

    def test_get_article(self):
        self.client.logout()
        url = reverse('article-detail',
                      kwargs={'pk': self.test_article.id})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data.get('content'),
                         self.test_article.content
                         )

    def test_update_article(self):
        self.client.force_login(self.normal_user)
        url = reverse('article-detail', args=[self.test_article.id])
        new_content = {'name': '测试更改文章标题',
                       'content': '测试更改文章内容',
                       }
        res = self.client.put(url, data=new_content)
        self.assertEqual(res.status_code, 200, res.data)
        self.assertEqual(res.data.get('content'),
                         new_content['content'],
                         res.data
                         )
        new_article = Article.objects.get(pk=self.test_article.id)
        self.assertEqual(res.data.get('content'),
                         new_article.content,
                         new_article.content
                         )

    def test_delete_article_with_wrong_person(self):
        self.client.logout()
        url = reverse('article-detail',
                      kwargs={'pk': self.test_article.id})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, 403)
