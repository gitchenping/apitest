
import requests
import json
import random,time

headers={"Content-Type":"application/json"}


datadict={
    "custId": 50263048,
    "grandOrderId": 2213035351045,
    "totalBarginPrice": 5300,
    "addressIds": [
        "9000",
        "111",
        "1",
        "1110101",
        "1110101"
    ],
    "orderIp": "127.0.0.1",
    "detailAddress": "放弃了",
    "submitGapTime": 6556,
    "registerDate": 1517241600000,
    "registerMobile": "13612345678",
    "registerEmail": "test@dangdang.com",
    "registerIp": "192.168.0.1",
    "fromPlatform": 0,
    "mobile": "13523493530",
    "userAction": [
        "/checkout/index",
        "/consignee/custAddress",
        "/order/getInfo",
        "/paymentnew/getAll",
        "/shipment/get",
        "/checkout/renderOver"
    ],
    "payablePrice": 5300,
    "couponAmount": 0,
    "orderTime": "2020-06-29 17:01:50.00",
    "custEmail": "email@dangdang.com",
    "deviceId": "F4F3D74B063119737F36A17802CB1906",
    "permanentId": "20171010150507552306127358788982574",
    "receiverName": "查无此人",
    "receiverTel": "023-1684302",
    "identityNum": "20170626163342919346675761",
    "mobileImei": "869315021543261",
    "mobileImsi": "460030137842941",
    "mobileMac": "88:28:b3:48:bc:fe",
    "tongdunDeviceid": "5edb3c1548f736354a86255228c881b4",
    "shumeiDeviceid": "20170626163341544f145ea4fe972834aa8d2c27495f3b200430c32c4b0677",
    "modified": False,
    "orderInfos": [
         {
            "payType": 1,
            "shopId": 0,
            "shipType": 1,
            "parentOrderId": 2213035351045,
            "invoiceTitle": "北京当当网信息技术有限公司",
            "orderType": 0,
            "paymentProviderId": 79,
            "shopType": 0,
            "isLargeOrder": 0,
            "packageOrderInfos": [
                {
                    "orderId": 2213035351045,
                    "shippingFee": 500,
                    "bargainPriceTotal": 1500,
                    "amountInfos": [
                        {
                            "amountType": 2,
                            "amount": 5000,
                            "relationId": "ddb",
                            "couponApplyId": "11078"
                        },
                        {
                            "amountType": 10,
                            "amount": 1200,
                            "relationId": "2341123"
                        }
                    ],
                    "promotionInfos": [
                        {
                            "promotionType": 3,
                            "promotionId": 341805
                        }
                    ],
                    "productInfos": [
                        {
                            "productId": 60186300,
                            "mainProductId": 60186299,
                            "categoryPath": "58.62.18.04.00.00",
                            "vipPrice": 5000,
                            "productCount": 1,
                            "virtualProducts": []
                        },
                        {
                            "productId": 249027843,
                            "mainProductId": 0,
                            "categoryPath": "58.62.19.04.00.00",
                            "vipPrice": 5920,
                            "virtualProducts": [
                                {
                                    "productId": 6984813,
                                    "mainProductId": 0,
                                    "categoryPath": "58.62.19.04.00.00",
                                    "vipPrice": 100,
                                    "productCount": 1
                                },
                                {
                                    "productId": 94198321,
                                    "mainProductId": 0,
                                    "categoryPath": "58.62.19.04.00.00",
                                    "vipPrice": 100,
                                    "productCount": 1
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    ]
}

url='http://10.255.255.93:8081/antifraud/api/grandorders'



custidlist=['286429995','720003166']

for i in range(10000,12000):
    datadict['custId']  = i%2 and custidlist[0] or custidlist[1]
    datadict["grandOrderId"]=2213035351049+i
    datadict['orderInfos'][0]['parentOrderId']=2213035351049+i
    datadict['orderInfos'][0]['packageOrderInfos'][0]['orderId']=2213035351049+i

    sleeptime=0.2*random.randint(1,5)
    time.sleep(sleeptime)
    # print(datadict)
    jsondata=json.dumps(datadict)
    r=requests.post(url,data=jsondata,headers=headers)
    print(r.text)
