import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html><body><center>' + \
                      '<h1>Welcome</h1>' + \
                      'This is jkteuber\'s Web server.<br />' + \
                      '<a href="/content">Content Page</a><br />' + \
                      '<a href="/image">Image Page</a><br />' + \
                      '<a href="/file">File Page</a><br />' + \
                      '<a href="/form">Form Page</a><br />' + \
                      '</center></body></html>'
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_index_page():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html><body><center>' + \
                      '<h1>Welcome</h1>' + \
                      'This is jkteuber\'s Web server.<br />' + \
                      '<a href="/content">Content Page</a><br />' + \
                      '<a href="/image">Image Page</a><br />' + \
                      '<a href="/file">File Page</a><br />' + \
                      '<a href="/form">Form Page</a><br />' + \
                      '</center></body></html>'
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_content_page():
    conn = FakeConnection("GET /content HTTP/1.0\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html><body><center>' + \
                      '<h1>Welcome to the content page!</h1>' + \
                      '</center></body></html>'
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_file_page():
    conn = FakeConnection("GET /file HTTP/1.0\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html><body><center>' + \
                      '<h1>Welcome to the file page!</h1>' + \
                      '</center></body></html>'
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_image_page():
    conn = FakeConnection("GET /image HTTP/1.0\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html><body><center>' + \
                      '<h1>Welcome to the image page!</h1>' + \
                      '</center></body></html>'
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_form_page():
    conn = FakeConnection("GET /form HTTP/1.0\r\n")
    expected_return = "HTTP/1.0 200 OK\r\n" + \
                      "Content-type: text/html\r\n" + \
                      "\r\n" + \
                      "<form action='/submit' method='GET'>" + \
                      "<input type='text' name='firstname'>" + \
                      "<input type='text' name='lastname'>" + \
                      "<input type='submit' name='Submit'>" + \
                      "</form>"
    print expected_return
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_submit_page():
    conn = FakeConnection("GET /submit?firstname=Joshua&lastname=Teuber HTTP/1.0\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      'Hello Mr. Joshua Teuber.'
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_post_response():
    conn = FakeConnection("POST /?firstname=Joshua&lastname=Teuber HTTP/1.0\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html><body>' + \
                      '<h1>You have sent a POST request</h1>' + \
                      'Hello Mr. Joshua Teuber.' + \
                      '</body></html>'
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
