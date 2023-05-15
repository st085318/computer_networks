from io import BytesIO
from requests import post, Response
from tkinter import Canvas, Menu, Tk
from typing import Optional
import os
import pickle
import socket

from PIL import Image


class Point:
    def __init__(self, x: Optional[int] = None, y: Optional[int] = None):
        self.x = x
        self.y = y

class Sender:
    def __init__(self, host = '127.0.0.1', port = '5000') -> None:
        self.socket_client =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect((host, port))
        
    def send(self, data):
        send_data = pickle.dumps(data)
        self.socket_client.sendall(send_data)


class DrawingApp:
    width = 500
    height = 400
    color_fg = 'black'
    color_bg = 'white'
    pen_width = 5
    path = './client/'
    filename = 'canvas.jpg'

    def __init__(self, master: Optional[Tk] = None, sender: Sender = None) -> None:
        self.master = master
        self.cur_pos = None

        self.canvas = Canvas(
            self.master,
            width=self.width,
            height=self.height,
            bg=self.color_bg
        )
        self.sender = sender
        self.canvas.pack(fill='both', expand=True)

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def paint(self, position: Point) -> None:
        if self.cur_pos:
            self.canvas.create_line(
                self.cur_pos.x,
                self.cur_pos.y,
                position.x,
                position.y,
                width=self.pen_width,
                fill=self.color_fg,
                capstyle='round',
                smooth=True,
            )

        self.cur_pos = position
        self.save_canvas()
        self.post_canvas()

    def reset(self, position: Point) -> None:
        self.cur_pos = None
        self.save_canvas()
        self.post_canvas()

    def save_canvas(self) -> None:
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        postscript = self.canvas.postscript(colormode='color')
        image = Image.open(BytesIO(postscript.encode('utf-8')))
        image.save(self.path + self.filename)

    def post_canvas(self) -> None:
        image = open(self.path + self.filename, 'rb').read()
        self.sender.send(image)

if __name__ == '__main__':
    root = Tk()
    sender = Sender(port=5000)
    DrawingApp(root, sender)
    root.title('Client')
    root.mainloop()