# 代码生成时间: 2025-10-09 20:37:46
from pyramid.config import Configurator
from pyramid.response import Response
import requests
from urllib.parse import urlparse


# 定义一个函数来检测URL是否有效
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
# 扩展功能模块

# 定义一个函数来获取CDN内容
def get_cdn_content(url):
    """
    从CDN获取内容的函数。
    
    参数:
    - url: 要获取内容的CDN URL
    
    返回值:
    - 如果成功获取内容，返回Response对象；否则返回错误信息。
    """
    if not is_valid_url(url):
        return Response("Invalid URL", status=400)
    try:
# 添加错误处理
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        return Response(response.content, content_type=response.headers['Content-Type'], request_url=response.url)
    except requests.RequestException as e:
        return Response(f"Error fetching CDN content: {e}", status=500)

# 配置Pyramid应用
def main(global_config, **settings):
    """
    Pyramid WSGI应用的入口函数。
    """
    config = Configurator(settings=settings)
    config.include('.pyramid_route')
    config.add_route('get_cdn_content', '/get_cdn_content')
    config.add_view(get_cdn_content, route_name='get_cdn_content')
    return config.make_wsgi_app()
# 增强安全性

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    with make_server('0.0.0.0', 6543, main) as server:
        print("Serving on 0.0.0.0 port 6543...")
        server.serve_forever()