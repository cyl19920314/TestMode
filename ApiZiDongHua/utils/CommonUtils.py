import json
import os

from utils.DataUtils import DataUtils
from utils.requestsutils import RequestsUtils
from utils.reportutils import ReportUtils
from jsonpath_rw import parse


# 自动化测试Baser工具类
class CommonUtils:
    def __init__(self):
        self.caseList = []

    # 读取所有用例所在文件夹方法得到所有用例路径
    def getCaseFile(self, path="../data"):
        # 定义空列表存放所有用例文件路径
        fileList = []
        # 扫描文件夹中所有的.xls文件和.xlsx文件
        list = os.listdir(path)
        # 循环过滤文件去除不是用例文件的其他文件
        for file in list:
            # 判断是否是用例文件不是的不做保留路径操作,是用例文件的保存到fileList列表中
            if file.endswith(".xls") or file.endswith(".xlsx"):
                # 路径格式为文件夹地址+"/"+文件名称
                fileList.append(path + "/" + file)
                # 返回用例文件路径列表
        return fileList

    # 比较预期结果和实际结果
    def compareResult(self, expectResult, actualResult):
        # 每个接口必须有status  msg
        if expectResult != None and expectResult != {} and actualResult != None and actualResult != {}:
            # 比较status还有msg
            if expectResult.get("status") == actualResult.get("status") and (
                        expectResult.get("msg") == actualResult.get(
                        "msg")):
                # 如果匹配判断预期结果和返回结果一致返回True
                return True
            else:
                # 如果匹配判断预期结果和返回结果不一致返回False
                return False
        else:
            # 如果读取到的信息和获取到的信息有一方为空直接返回False
            return False

    # 执行所有的用例文件
    def executeAllFile(self, path="../data"):
        # 得到所有用例路径列表
        fileList = self.getCaseFile(path)
        # 遍历所有的用例文件路径列表
        for caseFile in fileList:
            # 执行当前的文件
            self.executeSingleFile(caseFile)

    # 执行单个用例文件
    def executeSingleFile(self, file):
        # 创建Excel测试用例信息工具类DataUtils对象用于调取DataUtils工具类中的读取方法和回写测试结果的方法等
        dataUtils = DataUtils(file=file)
        # 创建网络请求工具类RequestsUtils对象用来调用执行验证用例读URL对应的网络请求
        requestUtils = RequestsUtils()
        # 循环遍历测试用例读取出来的所有测试用例条数
        for row in range(1, dataUtils.getCaseCount()):
            # 获取每一行的用例
            case = dataUtils.getCase(row)
            # 判断当前case是否有依赖
            if case["dept_id"] != None and case["dept_id"] != "":
                dept_no = int(case["dept_id"])
                # 根据dept_no获取所依赖接口的实际结果
                dept_case = dataUtils.getCase(dept_no)
                # 获取所依赖case的实际结果
                actual_result = dept_case["actual_result"]
                # 根据匹配规则，提取出参数来..
                regex = case["dept_field"]
                dept_params_value = self.getDeptParmas(actual_result, regex)
                # 获取依赖的参数名称
                dept_params = case["dept_params"]
                # 拼接依赖参数code
                case["params"][dept_params] = dept_params_value
                # 输出到控制台拼接后的参数
                # print(case["params"])

            # 执行当前的用例
            actualResult = requestUtils.doRequests(url=case["url"],
                                                   method=case["method"],
                                                   paramsType=case["paramsType"],
                                                   params=case["params"],
                                                   headers=case["headers"],
                                                   json=case["json"],
                                                   files=case["file_path"])
            # 转换返回结果 json.dumps 或 json.load一样转换成字典格式处理 转换格式时出现乱码问题
            stractaulResult = json.dumps(actualResult, ensure_ascii=False, indent=4)
            # 回写实际结果
            dataUtils.setCaseActualResult(row, actualResult)
            # 和预期结果做比较
            isPassed = self.compareResult(case["expect_result"], actualResult)
            # 回写是否通过row代表就是当前测试的用例行数
            dataUtils.setCaseIsPassed(row, isPassed)
            # 添加用例到读取的用例信息拼接完整是否测试通过
            case["is_pass"] = isPassed
            # 将所有的用例放到caseList中用于报告生成
            case["file_name"] = file
            self.caseList.append(case)
            # 发送测试报告到邮箱
            # reportutils.export_report(self.caseList)

    # 获取所有用例执行的信息
    def getCaseExcuteInfo(self):
        return self.caseList

    # 导出所有测试报告方法
    def exportReport(self):
        # 创建报告工具类对象
        reportUtils = ReportUtils()
        # 调取创建报告方法
        reportUtils.export_report(self.caseList)

    # 根据规则，到字典中提取参数dict字典格式regex提取格式
    def getDeptParmas(self, dict, regex):
        # 设置提取格式
        json_exe = parse(regex)
        # 获取返回结果
        result = json_exe.find(dict)
        # 提取依赖参数code
        params = [match.value for match in result][0]
        # 返回依赖参数
        return params


if __name__ == '__main__':
    # 创建执行用例工具类对象 可以指定路径查找 默认路径"../data"
    commonUtils = CommonUtils()
    # 执行指用例文件执行执行单个用例的路径"../data/case1.xls"
    # commonUtils.executeSingleFile("../data/case1.xls")
    # 执行所有用例文件指定执行用例的文件路径
    commonUtils.executeAllFile("../data")
    commonUtils.exportReport()
