import unittest

from utils import log
from utils.CommonUtils import CommonUtils


class TestCase_test_case(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # 执行所有文件
    def testAllFile(self):
        log.logger().info("=======开始执行所有测试用例文件=======")
        # 创建测试工具类对象
        commonUtils = CommonUtils()
        # 调用测试所有用例方法传入要执行用例的文件夹路径
        commonUtils.executeAllFile("../data")
        # 调用发送报告方法将测试结果发送到指定邮箱
        commonUtils.exportReport()
    # 执行单个文件
    def testSingleFile(self):
        log.logger().info("=======开始执行单个测试用例文件=======")
        # 创建测试工具类对象
        commonUtils = CommonUtils()
        # 调用测试所有用例方法传入要执行用例文件路径
        commonUtils.executeSingleFile("../data/case1.xls")
        # 调用发送报告方法将测试结果发送到指定邮箱
        commonUtils.exportReport()


if __name__ == '__main__':
    unittest.main()
