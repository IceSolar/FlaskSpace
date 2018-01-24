# -*- coding:utf-8 -*-
import sys
import json
__author__ = 'rudolf_han'
def api_request(http, api_url, head, params, method, logger, resp_type='json'):
    logger.info(":请求链接：{api_url}".format(api_url=api_url))
    logger.info(":请求方法：{method}".format(method=method))
    logger.info(":请求头：{head}".format(head=head))
    logger.info(":请求参数：{params}".format(params=json.dumps(params, indent=4, sort_keys=False, ensure_ascii=False)))


    if method.upper() == 'POST':
        resp_obj = http.http_post(api_url, head, params)

    elif method.upper() == 'GET':

        resp_obj = http.http_get(api_url, head, params)

    else:
        logger.error(': 暂不支持该请求方法！！！')
        sys.exit()

    if resp_type.upper() == 'JSON':

        resp_result = http.get_json_data(resp_obj)

    else:
        resp_result = http.get_content_data(resp_obj)

    logger.info(":请求返回结果：{resp_result}".format(resp_result=json.dumps(resp_result, indent=4, sort_keys=False, ensure_ascii=False)))
    return resp_result



