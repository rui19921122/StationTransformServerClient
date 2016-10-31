from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from collections import defaultdict
import json


def get_item_by_id_from_list(_id, _list):
    if _list:
        for i in _list:
            if i.get('id') == _id:
                return i
    _list.append({'id': _id, 'children': []})
    return _list[-1]


# Create your models here.

class MenuPickle(models.Model):
    json = models.TextField(verbose_name='字符数据')
    update_date = models.DateTimeField(auto_now_add=True)

    @classmethod
    def update_menu_json(cls):
        obj = []
        not_root_menus = Menu.objects.filter(parent__isnull=False)
        root_menus = Menu.objects.filter( parent__isnull=True)
        for root_menu in root_menus:
            obj.append({'id': root_menu.id, 'children': []})
        for not_root_menu in not_root_menus:
            _path = []  # 子节点与父节点的遍历索引
            _target = not_root_menu
            while _target.parent:
                _target = _target.parent
                _path.append(_target.id)
            _target_object = obj
            for i in reversed(_path):
                _target_object = get_item_by_id_from_list(i, _target_object)['children']
            _target_object.append({'id': not_root_menu.id, 'children': []})
        cls.objects.create(
            json=json.JSONEncoder().encode(obj)
        )

    @staticmethod
    def get_menu():
        _json = MenuPickle.objects.last()
        if _json:
            return json.JSONDecoder().decode(_json.json)
        else:
            return []


class Menu(models.Model):
    """
    目录，权限控制颗粒化到具体菜单
    """
    name = models.CharField(max_length=50,
                            verbose_name='目录名称',
                            )
    create_time = models.DateTimeField(verbose_name='创建时间',
                                       auto_now_add=True
                                       )
    owner = models.ForeignKey(User,
                              verbose_name='拥有人',
                              related_name='owner_menus',
                              )
    parent = models.ForeignKey('self',
                               verbose_name='父项名称',
                               null=True,
                               blank=True
                               )
    administrators = models.ManyToManyField(User,
                                            verbose_name='管理员',
                                            blank=True,
                                            related_name='managed_menus'
                                            )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '目录'
        verbose_name_plural = '目录列表'
        ordering = ['create_time']
        unique_together = ['parent','name']

    def get_parent(self):
        """
        获取父项
        :return: 父项，如无父项则引发ObjectNotFound错误
        :rtype: Menu
        """
        parent = self.parent
        if parent:
            return parent
        else:
            raise ObjectDoesNotExist("未发现父项")

    def get_children(self):
        """
        返回下一层子项,以列表形式
        :return: 子项
        :rtype: Menu[]
        """
        return Menu.objects.filter(parent=self)

    def save(self, *args, **kwargs):

        super(Menu, self).save(*args, **kwargs)
        MenuPickle.update_menu_json()
