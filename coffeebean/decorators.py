# encoding: utf-8
"""
公共装饰器
@author Yuriseus
@create 2016-5-11 14:59
"""
import functools
import json
import tornado.web
from concurrent.futures import ThreadPoolExecutor

from multiprocessing import cpu_count
from tornado.ioloop import IOLoop

from .cache import Cache
from .valid.validate import ValidateForm
from .valid.validate import ValidateParam

cache = Cache.current()


def cacheable(timeout=60):
    """
    缓存装饰器，在service层
    示例：@cacheable(timeout=CacheType.DEFAULT, key="user_info")
    如果key为None,则根据函数名称、参数自动生成key
    :param timeout: 缓存默认有效期
    """
    def handle_func(func):
        def wrapper(*args, **kwargs):
            func_name = str(func.__name__)
            cache_key = _gen_cache_key(func_name, args, kwargs)
            if cache.has_key(cache_key):
                result = cache.get(cache_key)
            else:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout=timeout)
            return result
        return wrapper
    return handle_func


def _gen_cache_key(func_name, args, kwargs):
    key_rule = '{0}_{1}_{2}'
    arg_list = []
    for index, arg in enumerate(args):
        if index > 0:    # 第一个参数为类对象
            arg_list.append(str(arg))
    kwargs_list = []
    for key in kwargs:
        kwargs_list.append(str(kwargs[key]))
    return key_rule.format(func_name, '_'.join(arg_list), '_'.join(kwargs_list))


validate_param = ValidateParam()
validate_form = ValidateForm()


def valid(cfg, is_body_arg=False):
    """
    数据验证器，在handler层，在service不再验证参数
    示例：@valid(cfg={'name': {'type': 'string', 'required': True}})
    @param cfg验证配置,dict类型
    @param is_body_arg 是否为请求体参数
    """
    def handle_func(func):
        def wrapper(*args, **kwargs):
            if not cfg:
                pass
            else:
                request_handler = None
                for index, arg in enumerate(args):
                    if index == 0:    # 第一个参数为类对象
                        request_handler = arg
                param_dict = {}
                for param_name in cfg:
                    if is_body_arg:
                        param_dict[param_name] = request_handler.get_body_argument(param_name, None)
                    else:
                        param_dict[param_name] = request_handler.get_argument(param_name, None)
                is_valid, error_msg = validate_form.is_valid(param_dict, cfg)
                if is_valid:
                    return func(*args, **kwargs)
                else:
                    response = {'success': False, 'errcode': 'INVALID_ARGUMENTS', 'error_msg': error_msg}
                    request_handler.finish(json.dumps(response, ensure_ascii=False))
        return wrapper
    return handle_func


EXECUTOR = ThreadPoolExecutor(max_workers=cpu_count())


def unblock(http_method):
    # 必须添加该装饰器，表明当前方法结束后，并不finish该请求
    # Tornado请求执行的流程默认是: initialize()->prepare()->http_method(get/post等)->finish()
    # 当用unblock装饰器装饰后，http_method实际是执行下面的_wrapper()方法，在_wrapper中我们只是将原始的
    # http_method提交给线程池处理，所以还没有执行完该http_method，所以还不能finish该请求
    @tornado.web.asynchronous
    @functools.wraps(http_method)
    def wrapper(self, *args, **kwargs):
        # 以下的callback必须在主线程执行
        # self.write(),self.finish()等都不是线程安全的
        def callback(future):
            data, response_code = future.result()
            self.write_response(data, response_code=response_code)
        _future = EXECUTOR.submit(functools.partial(http_method, self, *args, **kwargs))
        IOLoop.current().add_future(_future, callback)
    return wrapper


def async_execute(func):
    """
    放在线程池中异步执行
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        future = EXECUTOR.submit(functools.partial(func, self, *args, **kwargs))
        func_callback = kwargs.pop('callback', None)
        if func_callback:
            IOLoop.current().add_future(future, func_callback)
    return wrapper


if __name__ == '__main__':
    print('{0}_{1}_{2}'.format(1, 2, 3))
