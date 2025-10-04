# 代码生成时间: 2025-10-05 02:59:19
from pyramid.config import Configurator
from pyramid.response import Response
import psutil

# MemoryUsageAnalyser class handles the memory usage analysis
class MemoryUsageAnalyser:
    def __init__(self):
        self.memory = psutil.virtual_memory()

    def get_memory_usage(self):
        """
        Get the current memory usage as a percentage.
        Returns:
            float: The percentage of memory used.
        """
        return self.memory.percent

# Pyramid route setup
def memory_usage(request):
    analyser = MemoryUsageAnalyser()
    try:
        memory_usage_percent = analyser.get_memory_usage()
        return Response(f"Memory usage is at {memory_usage_percent}%")
    except Exception as e:
        return Response(f"Error: {str(e)}", status=500)

# Initialize Pyramid
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_route('memory_usage', '/memory_usage')
    config.add_view(memory_usage, route_name='memory_usage')
    app = config.make_wsgi_app()
    return app

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main({})
    server = make_server('0.0.0.0', 6543, app)
    print('Serving on port 6543...')
    server.serve_forever()