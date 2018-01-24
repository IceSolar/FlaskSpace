
from optparse import OptionParser

__author__ = 'rudolf_han'

def OptionArgs():
    parser = OptionParser(usage="usage:%prog [optinos] filepath")
    parser.add_option("-R", "--run", action="store",
                      dest="run",
                      default=None,
                      help="运行配置ID"
    )
    # parser.add_option("-P", "--project",
    #                   action="store",
    #                   dest="project",
    #                   default=False,
    #                   help="项目名称, 当-r 为 1 时 整个项目运行,多个项目名使用逗号分隔，-r 等于2 时，项目下所有的测试计划, -r 为 3 时 运行项目下所有的测试套件"
    # )
    # parser.add_option("-p", "--plan",
    #                   action="store_true",
    #                   dest="paln_name",
    #                   default=False,
    #                   help="计划名称 指定计划名称,多个计划名称使用逗号分隔"
    # )
    (options, args) = parser.parse_args()
    return options, args