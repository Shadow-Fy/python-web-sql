# -*- coding:utf-8 -*-
# 自定义分页主键
from django.utils.safestring import mark_safe


class PAGE(object):
    def __init__(self, request, queryset, page_size=10, plus=5, page_param="page"):
        """
        :param request: 进入这个页面时的request，请求对象
        :param queryset: 符合条件的对象，就是经过搜索筛选之后仍符合要求的数据
        :param page_size: 每页发的那个多少行数据
        :param plus: 分页时显示本页前后plus页的页码
        :param page_param: 再url中传递的获取分页的参数
        """
        # 获取当前页码
        page = request.GET.get(page_param, "1")
        # 防止页码为字母等等
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        # 获取总样本数
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count

        self.page = page
        # 防止搜索的时候超限
        if self.page < 1:
            self.page = 1
        if self.page > self.total_page_count:
            self.page = self.total_page_count

        self.plus = plus
        self.page_param = page_param
        self.page_size = page_size
        # 搜索结果数量为0时，保证self.start == 0
        self.start = (self.page - 1) * self.page_size * (self.page != 0)
        self.end = self.page * self.page_size

        # 搜索的时候分页会把原来搜索的条件替换掉，用这四行代码解决
        import copy
        querydict = copy.deepcopy(request.GET)  # 把包含原来所有参数的网址给弄过来
        querydict.mutable = True  # 这句话要看源码去找_mutable
        self.query_dict = querydict

        self.page_queryset = queryset[self.start: self.end]

    """生成html代码"""

    def create_html(self):
        # 显示当前页的前plus页和后plus页
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        page_str_list = list()
        self.query_dict.setlist(self.page_param, [1])
        # 首页
        page_str_list.append('<li><a href="?{}">首页&nbsp</a></li>'.format(self.query_dict.urlencode()))
        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页&nbsp</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页&nbsp</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        # 展示页
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}&nbsp</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)
        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            nex = '<li><a href="?{}">&nbsp下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            nex = '<li><a href="?{}">&nbsp下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(nex)
        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">&nbsp尾页&nbsp</a></li>'.format(self.query_dict.urlencode()))
        # 需要mark_safe后html才接受
        page_string = mark_safe("".join(page_str_list))
        return page_string

    """搜索页码"""

    def search(self):
        search_string = """
        <form method="get">
            <div class="input-group" style="width: 200px; float: right;">
                <input name = "page" type="text" class="form-control" style="width: 200px;" placeholder="页码">
                <span class="input-group-btn">
                    <button class="btn btn-default" type="submit">跳转</button>
                </span>
            </div>
        </form>
        """
        return mark_safe(search_string)
