# -*- condig: utf-8 -*-
from django.db import models

# 定义标签类
class Cate(models.Model):
    cid = models.IntegerField(blank=False, verbose_name='ID', unique=True)
    name = models.CharField(blank=False, max_length=64, verbose_name='名字')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cate'
        verbose_name_plural = "标签类别"

# 定义图书信息
class Book(models.Model):
    bid = models.IntegerField(blank=False,verbose_name='ID', unique=True)
    name = models.CharField(blank=False, max_length=64, verbose_name='名字')
    author =models.CharField(blank=True, max_length=500, verbose_name='作者')
    img = models.CharField(blank=True, max_length=500, verbose_name='封面图')
    tag = models.CharField(blank=True, max_length=500, verbose_name='标签')
    price = models.FloatField(blank=True, verbose_name="价格")
    publish_month = models.IntegerField(blank=True, verbose_name="出版距今月份")
    click = models.IntegerField(blank=True, verbose_name="点击次数")
    socre = models.FloatField(blank=True, verbose_name="评分")
    judge = models.IntegerField(blank=True, verbose_name="评价人数")
    rec_most =models.IntegerField(blank=True, verbose_name="力荐人数")
    rec_more =models.IntegerField(blank=True, verbose_name="推荐人数")
    rec_normal =models.IntegerField(blank=True, verbose_name="还行人数")
    rec_bad =models.IntegerField(blank=True, verbose_name="较差人数")
    rec_morebad =models.IntegerField(blank=True, verbose_name="很差人数")
    readed =models.IntegerField(blank=True, verbose_name="读过人数")
    reading =models.IntegerField(blank=True, verbose_name="正在读人数")
    readup =models.IntegerField(blank=True, verbose_name="想读人数")
    mess = models.CharField(blank=True, max_length=1000, verbose_name='出版信息')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'book'
        verbose_name_plural = "图书信息"

"""
    定义行为信息
    XXX 登录 系统
    XXX 查看 XXX  所属tag
"""
class History(models.Model):
    name = models.CharField(blank=False, max_length=64, verbose_name='名字')
    time = models.DateTimeField(blank=True,default="2008-12-12 12:12:00", verbose_name="点击时间")
    action = models.CharField(blank=False, max_length=64, verbose_name='行为')
    object = models.CharField(blank=False, max_length=64, verbose_name='对象')
    tag = models.CharField(blank=True, max_length=64, verbose_name='标签')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'history'
        verbose_name_plural = "行为信息"