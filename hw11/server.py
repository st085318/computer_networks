from cv2 import IMREAD_COLOR, imdecode
from jsonpickle import encode
from numpy import fromstring, uint8
from PIL import ImageTk, Image
import socket
import pickle


from tkinter import Canvas, Tk
from typing import Optional
import os



class ShowApp:
    width = 500
    height = 400
    color_fg = 'black'
    color_bg = 'white'
    pen_width = 5
    path = './server/'
    filename = 'canvas.jpg'


    def __init__(self, master: Optional[Tk] = None) -> None:
        self.master = master
        self.cur_pos = None

        self.canvas = Canvas(
            self.master,
            width=self.width,
            height=self.height,
            bg=self.color_bg
        )

        self.canvas.pack(fill='both', expand=True)


    def paint(self) -> None:
        self.image = ImageTk.PhotoImage(file=self.path + self.filename)
        self.canvas.create_image((250, 200), image=self.image)

def save_data(data: str) -> None:
        path = './server/'
        filename = 'canvas.jpg'

        image = fromstring(data, uint8)
        image = imdecode(image, IMREAD_COLOR)
        image = Image.fromarray(image.astype('uint8'), 'RGB')

        if not os.path.exists(path):
            os.makedirs(path)
        image.save(path + filename)



if __name__ == '__main__':
    app = Tk()
    sa = ShowApp(app)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 5000))
    server_socket.listen()
    
    print("Wait client")
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")
    
    def socket_get_info() -> None:
        global app
        data = conn.recv(100000)
        save_data(pickle.loads(data))
        sa.paint()
        app.after(10, socket_get_info)


    app.after(0, socket_get_info)
    app.mainloop()  