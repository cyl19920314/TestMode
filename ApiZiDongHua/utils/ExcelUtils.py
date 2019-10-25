# 读取Excel测试用例指定单元格工具类

import xlrd
from xlutils.copy import copy



class ExcelUtils:
    # 文件位置
    # 表格索引
    def __init__(self, file="../data/case1.xls", sheet_index=0):
        self.file = file
        self.sheet_index = sheet_index

    # 获取总的测试用例数量
    def getCaseCount(self):
        # 获取工作簿
        work_book = xlrd.open_workbook(self.file)
        # 获取工作表
        table = work_book.sheets()[self.sheet_index]
        # 获取总的行数
        return table.nrows

    # 根据行，根据列获取单元格的内容
    def getCellValue(self, row, col):
        # 获取工作簿
        work_book = xlrd.open_workbook(self.file)
        # 获取工作表
        table = work_book.sheets()[self.sheet_index]
        # 根据行和列获取单元格内容
        return table.cell_value(row, col)

    # 写入内容
    def writeCellValue(self, row, col, data):
        # 获取工作簿
        work_book = xlrd.open_workbook(self.file)
        # 复制一份
        copy_work_book = copy(work_book)
        # 获取表格
        table = copy_work_book.get_sheet(self.sheet_index)
        # 往表格中具体的单元格中写入内容
        table.write(row, col, data)
        # 保存表格
        copy_work_book.save(self.file)


# if __name__ == '__main__':
#     utils = ExcelUtils(file="../data/case1.xls")
#     print(utils.getCaseCount())
#     print(utils.getCellValue(2, 1))
#     #utils.writeCellValue(5, 1, "猫老大")
