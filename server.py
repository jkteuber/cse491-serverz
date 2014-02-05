#!/usr/bin/env python
import random
import socket
import time
import urlparse

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)

def handle_connection(conn):
    # Take in client request and seperate parts
    client_request = conn.recv(1000).split()
    urldata = urlparse.urlparse(client_request[1])

    # Sends the initial header to the client
    initial_response(conn)

    # Determine what is being requested
    if client_request[0] == 'GET':
        if urldata.path == '/':
            index_page(conn,urldata)
        elif urldata.path == '/content':
            content_page(conn,urldata)
        elif urldata.path == '/file':
            file_page(conn,urldata)
        elif urldata.path == '/image':
            image_page(conn,urldata)
        elif urldata.path == '/submit':
            submit_page(conn,urldata)
        elif urldata.path == '/form':
            form_page(conn, urldata)
    elif client_request[0] == 'POST':
        post_response(conn,urldata)    

def initial_response(conn):
    # Send the initial response to the client
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')

def index_page(conn, info):
    # Sends the index of the site to the client
    conn.send('<html><body><center>')
    conn.send('<h1>Welcome</h1>')
    conn.send('This is jkteuber\'s Web server.<br />')
    conn.send('<a href="/content">Content Page</a><br />')
    conn.send('<a href="/image">Image Page</a><br />')
    conn.send('<a href="/file">File Page</a><br />')
    conn.send('<a href="/form">Form Page</a><br />')
    conn.send('</center></body></html>')
    conn.close()

def content_page(conn, info):
    # Sends the content of the site to the client
    conn.send('<html><body><center>')
    conn.send('<h1>Welcome to the content page!</h1>')
    conn.send('</center></body></html>')
    conn.close()

def file_page(conn, info):
    # Sends the file page to the client
    conn.send('<html><body><center>')
    conn.send('<h1>Welcome to the file page!</h1>')
    conn.send('</center></body></html>')
    conn.close()

def image_page(conn, info):
    # Sends the image page to the client
    conn.send('<html><body><center>')
    conn.send('<h1>Welcome to the image page!</h1>')
    conn.send('</center></body></html>')
    conn.close()

def submit_page(conn, info):
    # Handles submitted info from form
    ## Needs test
    #Pulls out the names from submission
    info = urlparse.parse_qs(info.query)
    conn.send('Hello Mr. {0} {1}.'.format(info['firstname'][0],info['lastname'][0]))

def form_page(conn, info):
    # Sends the form info to the client
    ## Needs test
    conn.send("<form action='/submit' method='GET'>")
    conn.send("<input type='text' name='firstname'>")
    conn.send("<input type='text' name='lastname'>")
    conn.send("<input type='submit' name='Submit'>")
    conn.send("</form>")
    conn.close()

def post_response(conn, info):
    # Sends a response to the POST request
    info = urlparse.parse_qs(info.query)
    conn.send('<html><body>')
    conn.send('<h1>You have sent a POST request</h1>')
    conn.send('Hello Mr. {0} {1}.'.format(info['firstname'][0],info['lastname'][0]))
    conn.send('</body></html>')
    
    conn.close()

#  Code to run main function
if __name__ == '__main__':
    main()

