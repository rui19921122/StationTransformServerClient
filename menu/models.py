from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import json


# Create your models here.

class MenuPickle(models.Model):
    json = models.TextField(verbose_name='字符数据')
    update_date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def update_menu_json(obj: []):
        if not isinstance(obj, list):
            raise ValueError("{}不是list".format(obj))
        _json = json.JSONEncoder().encode(obj)
        print(_json)
        MenuPickle.objects.create(json=_json)

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
                            verbose_name='目录名称'
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
    enabled = models.BooleanField(default=True,
                                  verbose_name='启用标记'
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

    @staticmethod
    def get_all_menu_tree():
        """
        获取目录树
        :return:
        """
        # todo 完善获取目录树方法
        pass

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
        def get_element_by_id(id, obj):
            pass

        super(Menu, self).save(*args, **kwargs)
        menu_obj = MenuPickle.get_menu()
        if self.parent:
            parent = self.parent
            _list = [parent.id]
            while parent.parent:  # 如果父目录仍有父目录，则继续向上嵌套
                _list.append(parent.parent_id)
                parent = parent.parent
            _find_list = menu_obj
            for id in _list:
                for i in _find_list:
                    if i.get('id') == id:
                        _find_list = i.get('children')
                        break
            _find_list.append({
                'id': self.id,
                'children': []
            })
            MenuPickle.update_menu_json(menu_obj)


        else:
            menu_obj.append({'id': self.id,
                             'children': []
                             })
            MenuPickle.update_menu_json(menu_obj)
