
from djangobrowsertest.browsertest import BrowserTestCase
import urllib2

class TestAppRunningThroughBrowserTestCase(BrowserTestCase):
    
    def test_open_foo_page(self):        
        request_foo = urllib2.Request('http://localhost:8000/foo/')
        foo_content = urllib2.urlopen(request_foo).read()
        self.assertEquals('Hello! It is working', foo_content)

