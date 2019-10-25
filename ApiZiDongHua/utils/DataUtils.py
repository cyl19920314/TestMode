import json




# 读取Excel测试用例信息工具类
from utils.ExcelUtils import ExcelUtils
from utils.VarUtils import Var


class DataUtils:
    def __init__(self, file="../data/case1.xls"):
        # 要操作的用例路径赋值给我要传给ExcelUtils工具类
        self.file = file
        # 需要创建Excelutils工具类对象并且把要操作的用例路径传递到工具类中
        self.excelUtils = ExcelUtils(file=file)

    # 获取用例id 参数是行
    def getCaseID(self, row):
        # 返回读取到的用例ID
        return self.excelUtils.getCellValue(row, Var.REQUEST_ID)

    # 获取用例名称 参数是行
    def getCaseName(self, row):
        # 返回读取到的用例名称
        return self.excelUtils.getCellValue(row, Var.REQUEST_NAME)

    # 获取用例URL 参数是行
    def getCaseURL(self, row):
        # 返回读取到的用例URL
        return self.excelUtils.getCellValue(row, Var.REQUEST_URL)

    # 获取请求方式 参数是行
    def getCaseMethod(self, row):
        # 返回读取到的用例请求方式比如POST请求或者GET请求
        return self.excelUtils.getCellValue(row, Var.REQUEST_METHOD)

    # 获取请求方式参数类型
    def getCaseType(self, row):
        # 返回读取到的参数类型1代表普通参数2代表报文形式参数比如json
        return self.excelUtils.getCellValue(row, Var.REQUEST_TYPE)

    # 获取请求参数 参数是行
    def getCaseParams(self, row):
        try:
            # 将字符串转换成字典
            str = self.excelUtils.getCellValue(row, Var.REQUEST_PARAMS)
            '''
            读取的参数信息可能是
            {"email": "11@qq.com", "password": "123","username": "xxx"}
            用json把读取的字符串转换成字典格式
            '''
            return json.loads(str)
        # 抛出异常信息用于记录
        except Exception as e:
            # 如果发生异常返回except中的None或者{}空字典以免报错
            return {}

    # 获取文件上传路径 参数是行
    def getFilePath(self, row):
        # 直接返回读取到的要上传的文件路径
        return self.excelUtils.getCellValue(row, Var.FILE_PATH)
        # try:
        #     str = self.excelUtils.getCellValue(row, Var.FILE_PATH)
        #     # 抛出异常信息用于记录
        #     return json.loads(str)
        # except Exception as e:
        #     # 如果发生异常返回except中的None或者{}空字典以免报错
        #     return {}

    # 获取请求头信息 参数是行
    def getCaseHeaders(self, row):
        try:
            # 将字符串转换成字典类型
            str = self.excelUtils.getCellValue(row, Var.REQUEST_HEADERS)
            '''
            读取的参数信息可能是Cookie信息还有Content-Type编码格式等信息
            {"Cookie": "asljdolasjawehjoiasld", "Content-Type":"application/json;charset=utf-8"}
            用json把读取的字符串转换成字典格式
            '''
            return json.loads(str)
        # 抛出异常信息用于记录
        except Exception as e:
            # 如果发生异常返回except中的None或者{}空字典以免报错
            return {}

    # 获取用例依赖编号ID 参数是行
    def getCaseDependentNo(self, row):
        # 返回读取到的用例依赖编号ID
        return self.excelUtils.getCellValue(row, Var.REQUEST_DEPENDENT_NO)

    # 获取依赖的字段 参数是行
    def getCaseDependentField(self, row):
        # 返回读取到的依赖字段
        return self.excelUtils.getCellValue(row, Var.REQUEST_DEPENDENT_FIELD)

    # 获取当前接口依赖的参数名称 参数是行
    def getDependentParams(self, row):
        # 返回读取到的依赖参数名称信息
        return self.excelUtils.getCellValue(row, Var.REQUEST_DEPENDENT_PARAMS)

    # 获取用例预期结果 参数是行
    def getCaseExpectResult(self, row):
        try:
            str = self.excelUtils.getCellValue(row, Var.REQUEST_EXPECT_RESULT)
            '''
            读取的参数信息可能是
            {"status":200,"msg":"success","data":{"code":"W7LV"}}
            用json把读取的字符串转换成字典格式
            '''
            # str2 = json.loads(str)
            return eval(str)
            # 抛出异常信息用于记录
        except Exception as e:
            # 如果发生异常返回except中的None或者{}空字典以免报错
            return {}

    # 获取用例实际结果
    def getCaseActualResult(self, row):
        try:
            str = self.excelUtils.getCellValue(row, Var.REQUEST_ACTUAL_RESULT)
            return json.loads(str)
            # 抛出异常信息用于记录
        except Exception as e:
            # 如果发生异常返回except中的None或者{}空字典以免报错
            return {}

    # 回写实际结果
    def setCaseActualResult(self, row, data):
        try:
            # 先将字典转换成字符串，再写出
            str = json.dumps(data, ensure_ascii=False, indent=4)
            # 写入到xls或xlsx用例文件中
            self.excelUtils.writeCellValue(row, Var.REQUEST_ACTUAL_RESULT, str)
        except Exception as e:
            self.excelUtils.writeCellValue(row, Var.REQUEST_ACTUAL_RESULT, e)

    # 输出当前用例是否通过
    def setCaseIsPassed(self, row, isPassed=False):
        # 如果是True就代表通过否则是False没有通过
        if isPassed:
            # 返回通过
            self.excelUtils.writeCellValue(row, Var.REQUEST_IS_PASSED, "是")
        else:
            # 返回没通过
            self.excelUtils.writeCellValue(row, Var.REQUEST_IS_PASSED, "否")

    # 获取总的测试用例数量
    # 获取当前有多少用例
    def getCaseCount(self):
        # 获取工作簿一共有多少条要执行的用例
        return self.excelUtils.getCaseCount()

    # 获取是否通过
    def getIsPassed(self, row):
        return self.excelUtils.getCellValue(row,Var.REQUEST_IS_PASSED)

    # 获取用例每行的全部信息 参数是行row
    def getCase(self, row):
        # 创建一个空的字典存放读取出来的信息
        case = {}
        # 获取用例ID
        case["id"] = self.getCaseID(row)
        # 获取用例名称
        case["name"] = self.getCaseName(row)
        # # 获取用例URL
        case["url"] = self.getCaseURL(row)
        # 获取请求方式
        case["method"] = self.getCaseMethod(row)
        # 获取请求参数类型是普通参数还是报文形式比如json
        case["paramsType"] = self.getCaseType(row)
        # 获取请求参数类型是普通参数还是报文形式比如json
        case["json"] = self.getCaseParams(row)
        # 获取请求参数
        case["params"] = self.getCaseParams(row)
        # 获取文件上传路径
        case["file_path"] = self.getFilePath(row)
        # 获取请求头信息
        case["headers"] = self.getCaseHeaders(row)
        # 获取用例预期结果
        case["expect_result"] = self.getCaseExpectResult(row)
        # 获取用例实际结果
        case["actual_result"] = self.getCaseActualResult(row)
        # 获取用例依赖编号ID
        case["dept_id"] = self.getCaseDependentNo(row)
        # 存在接口依赖,取出依赖字段
        case["dept_field"] = self.getCaseDependentField(row)
        # 获取当前接口依赖的参数名称
        case["dept_params"] = self.getDependentParams(row)
        # 获取是否通过
        case["is_passed"] = self.getIsPassed(row)
        # 返回读取到的用例信息字典
        return case


# if __name__ == '__main__':
#     # dict = {"username": "zhangsan", "password": "123", "salery": None}
#     # # 将字段转换成字符串
#     # str = json.dumps(dict,ensure_ascii=False, indent=4)
#     # print(str)
#     # str = '{"username": "zhangsan", "password": "123", "salery": null}'
#     # # 将字符串转换成字典
#     # dict2 = json.loads(str)
#     # print(dict2, dict2["username"])
#
#     dataUtils = DataUtils()
#     case = dataUtils.getCase(1)
#     print(case)
#     print(case["url"])
