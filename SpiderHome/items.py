# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GdsqItem(scrapy.Item):
    station = scrapy.Field()
    time = scrapy.Field()
    water_level = scrapy.Field()
    flow = scrapy.Field()
    warning_water_level = scrapy.Field()


class GdwaterItem(scrapy.Item):
    thread = scrapy.Field()
    city = scrapy.Field()
    county = scrapy.Field()
    site = scrapy.Field()
    time = scrapy.Field()
    water_level = scrapy.Field()
    warning_level = scrapy.Field()
    water_potemtial = scrapy.Field()
    flood_limit_water_level = scrapy.Field()


class GdswItem(scrapy.Item):
    thread = scrapy.Field()
    stnm = scrapy.Field()  # 站名
    stcd = scrapy.Field()  # 站号
    tm = scrapy.Field()  # 时间
    z = scrapy.Field()  # 水位
    hnnm = scrapy.Field()  # 流域
    tend = scrapy.Field()  # 水势
    rvnm = scrapy.Field()  # 河流
    q = scrapy.Field()  # 流量


class GdepbItem(scrapy.Item):
    thread = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    cate = scrapy.Field()
    body = scrapy.Field()
    obj = scrapy.Field()
    location = scrapy.Field()
    doc_loc = scrapy.Field()


class App_gdepbItem(scrapy.Item):
    EntityId = scrapy.Field()
    YearWeek = scrapy.Field()
    SectionName = scrapy.Field()
    WeekRange = scrapy.Field()
    WaterSysName = scrapy.Field()
    RiverPartName = scrapy.Field()
    LevelID = scrapy.Field()
    OverItem = scrapy.Field()


class FjwItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()  # 获取当前url
    relateId = scrapy.Field()
    title = scrapy.Field()  # 获取标题
    city = scrapy.Field()  # 获取省级下一级城市名字
    region = scrapy.Field()  # 获取所在的区域
    district_name = scrapy.Field()  # 获取所在的街道
    house_desc = scrapy.Field()  # 获取房子的简介
    house_infor = scrapy.Field()  # 获取房子的信息
    contact = scrapy.Field()  # 获取获取联系人
    phone_number = scrapy.Field()  # 获取联系方式
    update_time = scrapy.Field()  # 获取更新时间
    img_urls = scrapy.Field()  # 图片下载地址
    img_path = scrapy.Field()  # 图片存储地址


class GzssItem(scrapy.Item):
    Thread = scrapy.Field()  # 数据存储编号 Thread
    RegistrationNumber = scrapy.Field()  # 注册号 Registration Number
    Name = scrapy.Field()  # 名称 Name
    LegalRepresentative = scrapy.Field()  # 法定代表人 Legal Representative
    Head = scrapy.Field()  # 负责人 Head
    Operators = scrapy.Field()  # 经营者 Operators
    Code = scrapy.Field()  # 社会信用代码 Social Credit Code
    MainCategory = scrapy.Field()  # 主营项目类别 Main Project Category
    BusinessScope = scrapy.Field()  # 经营范围 Business Scope
    LicenseScope = scrapy.Field()  # 许可经营范围 License Scope
    Home = scrapy.Field()  # 住所(经营场所) Home
    RegisteredCapital = scrapy.Field()  # 注册资本 Registered Capital
    CommercialBodyType = scrapy.Field()  # 商事主体类型 Commercial Body Type
    EstablishmentDate = scrapy.Field()  # 成立日期 Establishment Date
    OperatingPeriod = scrapy.Field()  # 营业期限 Operating Period
    IssuanceDate = scrapy.Field()  # 核发日期 Issuance Date
    RegistrationAuthority = scrapy.Field()  # 登记机关 Registration Authority
    State = scrapy.Field()  # 状态 State
    Notes = scrapy.Field()  # 备注 Notes
    doc_urls = scrapy.Field()
    doc_path = scrapy.Field()


class CSGXItem1(scrapy.Item):
    Thead = scrapy.Field()
    Jurisdiction = scrapy.Field()
    Street = scrapy.Field()
    Cellname = scrapy.Field()
    DeclarationBody = scrapy.Field()
    ReconstructedArea = scrapy.Field()
    Notes = scrapy.Field()


class CSGXItem2(scrapy.Item):
    Thead = scrapy.Field()
    Title = scrapy.Field()
    Date = scrapy.Field()
    Notes = scrapy.Field()
    Files = scrapy.Field()
