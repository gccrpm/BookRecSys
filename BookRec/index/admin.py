from django.contrib import admin

from index.models import Cate,History,Book

class CateAdmin(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ("cid", "name",)
    # 添加search bar，在指定的字段中searc
    search_fields = ("cid", "name",)
    # 页面右边会出现相应的过滤器选项
    # 排序
    ordering = ("cid",)

admin.site.register(Cate, CateAdmin)


class HistoryAdmin(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ("name","time","action","object","tag",)
    # 添加search bar，在指定的字段中search
    search_fields = ("name","time","action","object","tag",)
    # 页面右边会出现相应的过滤器选项
    list_filter = ("tag",)
    # 排序
    ordering = ("name",)
admin.site.register(History, HistoryAdmin)

class BookAdmin(admin.ModelAdmin):
    # 将字段全部显示出来
    list_display = ("bid", "name", "author", "img","tag","price","publish_month", "click", "socre", "judge","rec_most","rec_more","rec_normal","rec_bad","rec_morebad","readed","reading","readup",)
    # 添加search bar，在指定的字段中search
    search_fields = ("bid", "name", "author", "img","tag","price","publish_month", "click", "socre", "judge","rec_most","rec_more","rec_normal","rec_bad","rec_morebad","readed","reading","readup",)
    # 页面右边会出现相应的过滤器选项
    list_filter = ("tag",)
    # 排序
    ordering = ("bid",)
admin.site.register(Book, BookAdmin)
