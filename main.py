"""
    程序主入口:
    1、调用excel读取执行测试用例
    2、读取指定路径下所有的excel测试用例
    3、初始化日志器与关键类
"""
import os

from conf import log_conf
from excel_driver import excel_read

if __name__ == '__main__':
    # 创建日志生成器
    log = log_conf.get_log('conf/log.ini')
    # 定义测试用例集：
    cases = []
    # 获取指定路径下的所有测试用例：
    for path, dir, files in os.walk('./test_data'):
        # 保存获取到的所有测试用例文件：其实就是后缀名为.xlsx的文件
        for file in files:
            file_name = os.path.splitext(file)[0]
            # 获取文件后缀名
            file_type = os.path.splitext(file)[1]
            # 判断文件是否为excel
            if file_type == '.xlsx':
                # 判断是否需要该用例
                if 'old' not in file_name:
                    cases.append(path + '/' + file)
            else:
                log.info('文件类型错误:{}'.format(file))
        # 调用函数，运行测试用例
    for case in cases:
        log.info('正在运行{}测试用例'.format(case))
        excel_read.run(case, log)
