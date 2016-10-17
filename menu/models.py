from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Menu(models.Model):
    """
    目录
    """
    name = models.CharField(max_length=50,
                            verbose_name='目录名称'
                            )
    create_time = models.DateTimeField(auto_created=True,
                                       verbose_name='创建时间'
                                       )
    create_name = models.ForeignKey(User,
                                    verbose_name='创建人')
    parent = models.ForeignKey('self',
                               verbose_name='父项名称',
                               null=True,
                               blank=True
                               )
    enabled = models.BooleanField(default=True,
                                  verbose_name='启用标记'
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
        return self.parent

    def get_children(self):
        pass
