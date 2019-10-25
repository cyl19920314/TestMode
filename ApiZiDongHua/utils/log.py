# coding=utf-8
import logging
import time
import os
import logging.handlers

# log工具类
def logger(appName="test", rootstdout=True, handlerList=["I"]):
    log_fmt = "%(asctime)s --%(name)s [%(levelname)s]:\n%(message)s"
    c_fmt = "%(asctime)s --%(name)s [%(levelname)s]:\n%(message)s"
    date_format = "%Y-%m-%d %H:%M:%S %a"
    # 设置Console输出level
    logging.basicConfig(level=logging.DEBUG,
                        format=c_fmt,
                        datefmt=date_format,

                        )

    levels = []
    if isinstance(handlerList, list):
        if handlerList.__contains__("I") or handlerList.__contains__("Info"):
            levels.append("Info")
        if handlerList.__contains__("D") or handlerList.__contains__("Debug"):
            levels.append("Debug")
        if handlerList.__contains__("E") or handlerList.__contains__("Error"):
            levels.append("Error")
        if handlerList.__contains__("W") or handlerList.__contains__("Warning"):
            levels.append("Warning")
        if levels:
            stamp = time.strftime("%Y%m%d", time.localtime()) + ".log"
            logsdir = os.path.join(os.getcwd() + "/../logs")
            if os.path.exists(logsdir):
                for p in levels:
                    if os.path.exists(os.path.join(logsdir, p)):
                        pass
                    else:
                        os.mkdir(os.path.join(logsdir, p))
            else:
                os.mkdir(logsdir)
                for p in levels:
                    print(os.path.join(logsdir, p))
                    os.mkdir(os.path.join(logsdir, p))

            f_dict = {}
            for i in levels:
                filename = os.path.join(logsdir, i, stamp)
                f_dict[i] = filename
            logger = logging.getLogger(appName)

            for k, v in f_dict.items():
                handler = logging.handlers.RotatingFileHandler(filename=v, maxBytes=1024 * 1024 * 50, backupCount=5,
                                                               encoding="utf-8", delay=False)
                h_fmt = logging.Formatter(log_fmt)
                handler.setFormatter(h_fmt)
                if k == "E" or k == "Error":
                    handler.setLevel(logging.ERROR)
                elif k == "I" or k == "Info":
                    handler.setLevel(logging.INFO)
                elif k == "W" or k == "Warning":
                    handler.setLevel(logging.WARNING)
                elif k == "D" or k == "Debug":
                    handler.setLevel(logging.DEBUG)
                else:
                    raise NameError("check your logLevel Name is corrected or not")
                logger.addHandler(handler)
            logger.propagate = rootstdout
            return logger
        else:
            raise TypeError("check handlerList at least one corrected logLevel in:'Error','Info','Warning','Debug'")
    else:
        raise NameError("handlerList expected type is list but get type {}".format(type(handlerList).__name__))


if __name__ == "__main__":
    time.sleep(0.01)
    logger().info("file test")
