# -*- coding: utf-8 -*-
import scrapy
from exam.items import ExamItem, Student


class ExamSpider(scrapy.Spider):
    name = "exam"
    username = "1453xxx"
    password = "123123"
    allowed_domains = ["tongji.edu.cn"]
    start_urls = ['http://xuanke.tongji.edu.cn']

    def parse(self, response):
        self.logger.info("Visited %s", response.url)
        return scrapy.http.FormRequest.from_response(
            response,
            formdata={'goto': 'http://xuanke.tongji.edu.cn/pass.jsp',
                      'gotoOnFail': 'http://xuanke.tongji.edu.cn/deny.jsp',
                      'Login.Token1': self.username,
                      'Login.Token2': self.password,
                      'T3': ''
                      },
            callback=self.after_login
        )

    def after_login(self, response):
        return scrapy.Request("http://xuanke.tongji.edu.cn/tj_login/info.jsp", callback=self.get_info)

    def get_info(self, response):
        student = Student()
        student['username'] = response.xpath('//tr/td[2]/text()').extract()[0][1:]
        student['name'] = response.xpath('//tr/td[2]/text()').extract()[1][1:]
        # yield student
        return scrapy.Request(
            "http://xuanke.tongji.edu.cn/tj_login/redirect.jsp?" +
            "link=/tj_xuankexjgl/score/query/student/cjcx.jsp?" +
            "qxid=20051013779916&mkid=20051013779901&qxid=20051013779916",
            callback=self.parse_cj)

    def parse_cj(self, response):
        classes = response.xpath("//form/table[@id='T1']/tr")

        for item in classes:
            no = item.xpath('td[1]/div/font/text()').extract()
            name = item.xpath('td[2]/div/font/text()').extract()
            score = item.xpath('td[3]/div/font/text()').extract()
            update_time = item.xpath('td[9]/div/font/text()').extract()
            if len(score) is not 0:
                exam = ExamItem()
                exam['class_no']= no[0]
                exam['class_name'] = name[0]
                exam['class_score']= score[0]
                exam['class_update_time'] = update_time[0]
                print(no[0], name[0], score[0], update_time[0])
                yield exam
