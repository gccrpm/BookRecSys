# -*- condig: utf-8 -*-
from django.http import JsonResponse
from BookRec.settings import USER
from index.models import Cate, History, Book
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import time
from sklearn.externals import joblib
import numpy as np

"""
返回 用户和类别
"""
@csrf_exempt
def login(request):
    if request.method == "GET":
        users = USER
        tags = Cate.objects.all()
        return JsonResponse(
            {"code": 1, "data": {"users": users, "tags": [tag.name for tag in tags]}}
        )
    else:
        # 将用户信息写入session
        request.session["username"] = request.POST.get("username")
        request.session["tags"] = request.POST.get("tags")
        write_to_mysql(
            name=request.POST.get("username"),
            time=getLocalTime(),
            action="登录",
            object="系统",
            tag="",
        )
        return JsonResponse(
            {
                "code": 1,
                "data": {
                    "username": request.POST.get("username"),
                    "tags": request.POST.get("tags"),
                },
            }
        )

# 切换用户
def switchuser(request):
    if "username" in request.session.keys():
        uname = request.session["username"]
        # 删除新闻浏览表中的记录
        History.objects.filter(name=uname).delete()
        print("删除用户: %s 的点击记录 ..." % uname)
        del request.session["username"]  # 删除session
        del request.session["tags"]  # 删除session
        print("用户: %s 执行了切换用户动作，删除其对应的session值 ..." % uname)
    return JsonResponse({"code": 1, "data": {}})


# 首页模块，基于GBDT模型进行
def home(request):
    # 接口传入的page参数
    uname = request.GET.get("username")
    _page_id = int(request.GET.get("page"))
    tag = request.GET.get("rec")
    # 定义变量和结果
    _list = list()
    result = dict()
    result["code"] = 1
    result["data"] = dict()


    tags = Cate.objects.all()
    # tag为all，表示是为用户进行图书推荐
    if tag == "all":
        # 如果用户没有选择标签和用户没有产生任何行为，执行下边的逻辑
        if "tags" in request.session.keys() and request.session["tags"] == "" and History.objects.filter(name=uname).filter(~Q(tag="")).__len__() == 0:
            books = Book.objects.order_by("-socre").all()[:40]
            # 推荐
            total = books.__len__()
            for one in books:
                _list.append(
                    {
                        "id": one.bid,
                        "name": one.name,
                        "img": one.img,
                        "author": one.author,
                        "tag": one.tag,
                        "score": one.socre,
                        "judge": one.judge,
                    }
                )
        # 如果用户选择标签，执行下边的逻辑
        else:
            # 用户选择的标签
            chooose_tags = request.session["tags"].split(",") if "tags" in request.session.keys() else list()
            # 用户有点击行为的标签
            click_tags = [ one["tag"] for one in History.objects.filter(name=uname).values("tag").distinct()]
            # 拼接标签
            chooose_tags.extend(click_tags)
            chooose_tags = list (set(chooose_tags))

            # 用户已经点击过的图书 召回时进行过滤
            clicked_books =[ one["object"] for one in History.objects.filter(name=uname).values("object").distinct() ]
            # 初步召回数据集，每个标签下召回10本图书
            all_books = list()
            for tag in chooose_tags:
                one_books = Book.objects.filter(tag=tag).filter(~Q(name__in=clicked_books)).order_by("-socre")[:10]
                all_books.extend(one_books)
            # 加载模型
            gbdt = joblib.load('z-others/model/gbdt.model')
            # 对召回的数据进行排序
            sort_books_dict = dict()
            for book in all_books:
                features = [book.price,book.publish_month,book.click,book.socre,book.judge,book.rec_most,book.rec_more,book.rec_normal,book.rec_bad,book.rec_morebad,book.readed,book.reading,book.readup]
                pro = gbdt.predict_proba(np.array([features]))[0][1]
                sort_books_dict[book.bid] = pro
            books = sorted(sort_books_dict.items(), key = lambda one: one[1],reverse=True)
            # 推荐
            total = books.__len__()
            for one in books[:40]:
                one = Book.objects.filter(bid=one[0])[0]
                _list.append(
                    {
                        "id": one.bid,
                        "name": one.name,
                        "img": one.img,
                        "author": one.author,
                        "tag": one.tag,
                        "score": one.socre,
                        "judge": one.judge,
                    }
                )
    else: # 表示用户查看的是具体标签下的图书数据
        books = Book.objects.filter(tag=tag).order_by("-socre")
        total = books.__len__()
        for one in books[(_page_id - 1) * 20 : _page_id * 20]:
            _list.append(
                {
                    "id": one.bid,
                    "name": one.name,
                    "img": one.img,
                    "author": one.author,
                    "tag": one.tag,
                    "score": one.socre,
                    "judge": one.judge,
                }
            )
    result["data"]["books"] = _list
    result["data"]["total"] = total
    result["data"]["tags"] = [tag.name for tag in tags]
    return JsonResponse(result)


# 行为记录
def history(request):
    # 接口传入的page参数
    _page_id = int(request.GET.get("page"))
    result = dict()
    result["code"] = 1
    result["data"] = dict()
    _list = list()
    clicks = History.objects.filter(name=request.GET.get("username")).order_by("time")
    total = clicks.__len__()
    for one in clicks[(_page_id - 1) * 20 : _page_id * 20]:
        _list.append(
            {
                "name": one.name,
                "time": one.time,
                "action": one.action,
                "object": one.object,
                "tag": one.tag
            }
        )
    result["data"]["click"] = _list
    result["data"]["total"] = total
    return JsonResponse(result)

def one(request):
    _bid = int(request.GET.get("id"))
    one = Book.objects.filter(bid=_bid)[0]
    write_to_mysql(
        name=request.GET.get("username"),
        time=getLocalTime(),
        action="查看",
        object=one.name,
        tag=one.tag,
    )
    return JsonResponse(
        {
            "code": 1,
            "data": {
                "id": one.bid,
                "name": one.name,
                "img": one.img,
                "tag": one.tag,
                "click": one.click,
                "score": one.socre,
                "judge": one.judge,
                "rec_most": one.rec_most,
                "rec_more": one.rec_more,
                "rec_normal": one.rec_normal,
                "rec_bad": one.rec_bad,
                "rec_morebad": one.rec_morebad,
                "readed": one.readed,
                "reading": one.reading,
                "readup": one.readup,
                "mess": one.mess
            }
        }
    )


# 行为信息写入表
def write_to_mysql(name="", time="", action="", object="", tag=""):
    History(name=name, time=time, action=action, object=object, tag=tag).save()
    print("{} 在 {} {} {} ,{} ,写入数据库！".format(name, time, action, object, tag))


# 获取当前格式化的系统时间
def getLocalTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
