import os

import requests

# 网络请求工具类
from utils import log


class RequestsUtils:
    # 请求封装方法
    def doRequests(self, url=None, method=None, paramsType=None, params=None, headers={}, json=None, files=None):
        # 往头中添加cookie信息
        cookie = self.getCookies()
        # 判断获取到的Cookie信息不是None的情况加才添加Cookie
        if cookie != None:
            headers["Cookie"] = cookie

        # 根据methot请求类型做出选择是POST请求还是GET请求
        if method == "POST":
            # 调用POST请求
            return self.doPOST(url, paramsType, params, headers, json, files)
        else:
            # 调用GET请求
            return self.doGET(url, params, headers)

    # POST请求
    def doPOST(self, url, paramsType, params, headers, json, files):
        # post请求执行方法
        if int(paramsType) == 3:
            pic = {"pic": open(files, mode="rb")}
            result = requests.post(url=url, data=params, files=pic, timeout=10)
        elif int(paramsType) == 2:
            result = requests.post(url=url, headers=headers, json=json, timeout=10)
        else:
            result = requests.post(url=url, data=params, headers=headers, timeout=10)
        # 判断请求状态码如果是200请求成功做出相应操作
        if result.status_code == 200:
            # 提取headers 头信息中的Cookie信息
            self.setCookies(result.headers)
            # 如果返回不是json格式会抛出异常添加try
            try:
                # 返回json格式的返回结果
                return result.json()
            # 如果返回不是json格式会抛出异常添加except返回其他结果
            except:
                # 返回其他形式的信息
                return result.text
        else:
            # 添加log捕获异常错误信息
            log.logger().info("当前出错了,错误码是%d" % result.status_code)
            try:
                error = result.raise_for_status()
                # 添加异常捕获log
                log.logger().info("当前出错了错误信息是%s" % error)
            except Exception as e:
                # 添加异常捕获log
                log.logger().info("当前出错了错误信息是%s" % e)
            # 返回字典形式的信息以免报错
            return {}

    # GET请求
    def doGET(self, url, params, headers):
        # get请求执行方法
        result = requests.post(url=url, params=params, headers=headers, timeout=10)
        # 判断请求状态码如果是200请求成功做出相应操作
        if result.status_code == 200:
            # 提取headers 头信息中的Cookie信息
            self.setCookies(result.headers)
            # 如果返回不是json格式会抛出异常添加try
            try:
                # 返回json格式的返回结果
                return result.json()
            # 如果返回不是json格式会抛出异常添加except返回其他结果
            except:
                # 返回其他形式的信息
                return result.text
        else:
            # 添加log捕获异常错误信息
            log.logger().info("当前出错了,错误码是%d" % result.status_code)
            try:
                error = result.raise_for_status()
                # 添加异常捕获log
                log.logger().info("当前出错了错误信息是%s" % str(error))
            except Exception as e:
                # 添加异常捕获log
                log.logger().info("当前出错了错误信息是%s" % e)
            # 返回字典形式的信息以免报错
            return {}

    # 设置Cookie信息到cookie文件夹的cookie.txt文件中
    def setCookies(self, headers):
        # 获取Cookie信息
        cookie = headers.get("Set-Cookie")
        # 判断Cookie信息不为None才会写入
        if cookie != None:
            # 开启文件流写入Cookie信息
            stream = open("../cookie/cookie.txt", mode="w")
            # 执行写入
            stream.write(str(cookie))
            # 关闭写入文件流
            stream.close()

    # 读取cookie信息读取第一条
    def getCookies(self):
        # 先判断文件是否存在，如果文件存在读取打开cookie文件夹下的cookie.txt文件读取Cookie信息
        if os.path.exists("../cookie/cookie.txt"):
            # 开启读取文件流
            stream = open("../cookie/cookie.txt", mode="r")
            # 执行读取文件流
            cookie = stream.readline().strip()
            # 关闭读取文件流
            stream.close()
            return cookie
        else:
            return None

    # 测试代码 测试log可以把index修改成indexxxxx
# if __name__ == '__main__':
#     utils = RequestsUtils()
#     result = utils.doRequests("http://47.94.86.16/shop/index", method="GET")
#     # result = utils.doRequests('http://47.94.86.16/stest/user/upload.action', method="POST", paramsType=3,
#     #                         params={"username": "猫老大"}, files='C:\\Users\\lenovo\\Desktop\\新建文件夹 (2)\\123.jpg')
#     print(result)
