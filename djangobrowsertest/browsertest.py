# Code based on django_live_server_r8458.diff @  http://code.djangoproject.com/ticket/2879#comment:41

import unittest
import socket
import threading
from django.core.handlers.wsgi import WSGIHandler
from django.core.servers import basehttp
from django.conf import settings

class StoppableWSGIServer(basehttp.WSGIServer):
    """WSGIServer with short timeout, so that server thread can stop this server."""

    
    def server_bind(self):
        basehttp.WSGIServer.server_bind(self)
        self.socket.settimeout(1)
    
    def get_server(self):
        try:
            sock, adress = self.socket.accept()
            sock.settimeout(1)
        except socket.timeout:
            raise

class TestServerThread(threading.Thread):
    "Runs a http test server while the the tests are being ran"
    
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self._stopevent = threading.Event()
        self.started = threading.Event()
        self.error = None
        super(TestServerThread, self).__init__()
        
    def _setup_test_database(self):
        # Must do database stuff in this new thread if database in memory.
        from django.conf import settings
        if settings.DATABASE_ENGINE == 'sqlite3' \
            and (not settings.TEST_DATABASE_NAME or settings.TEST_DATABASE_NAME == ':memory:'):
            from django.db import connection
            db_name = connection.creation.create_test_db(0)
            # Import the fixture data into the test database.
            if hasattr(self, 'fixtures'):
                # We have to use this slightly awkward syntax due to the fact
                # that we're using *args and **kwargs together.
                call_command('loaddata', *self.fixtures, **{'verbosity': 0})
    
    def run(self):
        """Sets up test server and database and loops over handling http requests."""
        try:
            handler = basehttp.AdminMediaHandler(WSGIHandler())
            httpd = None
            while httpd is None:
                try:
                    server_address = (self.address, self.port)
                    httpd = StoppableWSGIServer(server_address, basehttp.WSGIRequestHandler)
                except basehttp.WSGIServerException, e:
                    if "Address already in use" in str(e):
                        self.port +=1
                    else:
                        raise e
            httpd.set_app(handler)
            self.started.set()
        except basehttp.WSGIServerException, e:
            self.error = e
            self.started.set()
            return
        
        self._setup_test_database()
        
        # Loop until we get a stop event.
        while not self._stopevent.isSet():
            httpd.handle_request()
        httpd.server_close()
        
       
    def join(self, timeout=None):
        """Stop the thread and wait for it to finish."""
        self._stopevent.set()
        threading.Thread.join(self, timeout)
        


class BrowserTestCase(unittest.TestCase):
    
    def setup_test_server(self, address='127.0.0.1', port=8000):
        """Creates a live test server object (instance of WSGIServer)."""
        self.server_thread = TestServerThread(address, port)
        self.server_thread.start()
        self.server_thread.started.wait()
        if self.server_thread.error:
            raise self.server_thread.error
    
    def stop_test_server(self):
        if self.server_thread:            
            self.server_thread.join()
            
    def setUp(self):
        self.setup_test_server()
        
    def tearDown(self):
        self.stop_test_server()
        
            
        
            
            
    

    
    