import requests
import re
import pymysql as pysql


class DouBan:
    def __init__(self, user, password, host='localhost', port=3306):
        self.url = "https://movie.douban.com/top250?start={}&filter="
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}
        self.sqlConnect(user, password, host, port)

    def dataGet(self, start):
        return requests.get(self.url.format(start), headers=self.headers).text

    def dataClean(self, html:str):
        result = []
        html = html.replace("\n", "")
        rep = re.compile('<div class="info">.*?</li>')
        for info in re.findall(rep, html):
            # 名字
            names = re.findall('<span class="title">(.*?)</span>', info)
            chineseName = names[0]
            if len(names)==2:
                englishName = names[1].replace("/", "").strip().replace("&nbsp;", "")
            else:
                englishName = "-"
            otherName = re.findall('<span class="other">(.*?)</span>', info)[0].strip("/").replace("&nbsp;", "")
            # 评分, 评价人数
            star = re.findall('<span class="rating_num".*?>(.*?)</span>', info)[0]
            starPeople = re.findall('<span>(.*?)人评价</span>', info)[0]
            starPeople = self.Format(starPeople)
            # 语录
            try:
                nidehanwang = re.findall('<span class="inq">(.*?)</span>', info)[0]
            except:
                nidehanwang = "-"
            # other
            others = re.findall('<p class="">(.*?)</p>', info)[0].strip().replace("/", "").split("&nbsp;&nbsp;")
            type = others[-1]
            country = others[-2]
            if len(others) == 4:
                direct = others[0].split(":")[-1].strip()
                others = others[1].split("<br>")
                year = others[-1].strip()
                actors = others[0].split(":")[-1]
            else:
                if "主演" not in others[0]:
                    direct = others[0].split("<br>")[0].split(":")[1]
                    year = others[0].split("<br>")[1].strip()
                    actors = "-"
            if len(str(year))>4:
                year = re.findall("([0-9]+)", year)[-1]
            result.append([chineseName, englishName, otherName,
                          direct, actors, year, country, type,
                          star, starPeople, nidehanwang])
        return result

    def sqlConnect(self, user, password, host, port):
        try:
            self.conn = pysql.connect(user=user, password=password, host=host, port=port)
        except Exception as e:
            print("数据库连接失败")
            exit(0)
        print("数据库连接成功!")
        self.cursor = self.conn.cursor()

        self.cursor.execute("create database if not exists test")
        self.cursor.execute("use test")
        try:
            self.cursor.execute("drop table App_moviesinfo")
        except:
            pass
        sql = '''
                create table if not exists App_moviesinfo (
                id int unsigned auto_increment,
                `zh_name` varchar(15),      # 中文名
                `en_name` varchar(70),      # 英文名
                `another_name` varchar(100),    # 别名
                `director` varchar(70),         # 导演
                `actor` varchar(50),            # 演员
                `release_year` int,             # 上映年份
                `release_country` varchar(30),  # 上映国家
                `type` varchar(30),                # 类型
                `score` char(3),                    # 评分
                `eval_number` varchar(10),             # 评价人数
                `quotation` varchar(50),            # 语录
                primary key (`id`))
            '''
        self.cursor.execute(sql)

    def sqlSave(self, datas:list):
        sql = '''
                insert into App_moviesinfo (
                `zh_name`, `en_name`, `another_name`, `director`, `actor`, `release_year`, `release_country`, `type`, `score`, `eval_number`, `quotation`
                ) value("{}", "{}", "{}", "{}", "{}", {}, "{}", "{}", "{}", "{}", "{}")
            '''
        for line in datas:
            newsql = sql
            for i in line:
                newsql = newsql.replace("{}", i, 1)
            self.cursor.execute(newsql)
        self.conn.commit()


    def Format(self, num):
        if len(str(num))>4:
            return str(round(int(num)/10000, 1))+"万"

    def run(self):
        for i in range(2):
            print("正在爬取第<{}>/<{}>页".format(i, 2))
            html = self.dataGet(i*25)
            data = self.dataClean(html)
            self.sqlSave(data)
        print("爬取成功!")
        self.conn.close()

if __name__ == '__main__':
    douban = DouBan(user='root', password='followheart1229')
    douban.run()
