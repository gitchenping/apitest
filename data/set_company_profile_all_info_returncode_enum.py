from enum import Enum

class SetCompanyProfileAllInfoReturnCodeEnum(Enum):
    SUCCESS=(0, "success")
    CUSTID_WRONG=(1, "custid不正确")
    COMPANY_LONG=(2,"cust_company的长度大于100")
    CONTRACTOR_LONG=(3, "cust_contractor的长度大于100")
    ADDRESS_LONG=(4,"cust_address的长度大于500")
    PROVINCE_TOWN_QUARTER_EMPTY=(5,"cust_province_id/cust_city_id/cust_town_id/cust_quarter_id 是空")


