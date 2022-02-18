from channels.generic.websocket import WebsocketConsumer

class EchoConsumer(WebsocketConsumer):
    # groups = ["broadcast"]

    def connect(self):
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            self.send(text_data=text_data + "-echo server")
        elif bytes_data:
            self.send(bytes_data=bytes_data)
       

    def disconnect(self, close_code):
        pass