#!/usr/bin/python
'''
 Author: Igor Maculan - n3wtron@gmail.com
 A Simple mjpg stream http server
'''
import cv2
from PIL import Image
import http.server
from socketserver import ThreadingMixIn
import time
import shutil
import os
from io import BytesIO
from http.server import BaseHTTPRequestHandler

capture = None


class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("getting " + self.path)
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            while True:
                try:
                    imgRGB = cv2.imread("stream/stream.jpeg")

                    jpg = Image.fromarray(imgRGB)
                    tmpFile = BytesIO()
                    jpg.save(tmpFile, 'JPEG')

                    self.wfile.write(bytes("--jpgboundary", "utf8"))

                    self.send_header('Content-type', 'image/jpeg')

                    self.send_header('Content-length', jpg.size)

                    self.end_headers()

                    jpg.save(self.wfile, 'JPEG')

                    time.sleep(0.5)
                except KeyboardInterrupt:
                    break
                except AttributeError:
                    print("No image to show", AttributeError)
            return
        if self.path.endswith('.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><head></head><body>')
            self.wfile.write('<img src="http://0.0.0.0:8080/cam.mjpg"/>')
            self.wfile.write('</body></html>')
            return


class ThreadedHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    """Handle requests in a separate thread."""


def main():
    global img
    try:
        copy_black_image()

        server = ThreadedHTTPServer(('0.0.0.0', 8080), CamHandler)
        print("server started")
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()


def copy_black_image():
    try:
        os.remove("/detection/stream/stream.jpeg")
    except OSError:
        print('file deleted')
    shutil.copy("/detection/stream/streamBlack.jpeg", "/detection/stream/stream.jpeg")


if __name__ == '__main__':
    main()
