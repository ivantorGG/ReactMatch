import sys

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.media_player = QMediaPlayer()
        self.media_player.setSource(QUrl.fromLocalFile("inst_vid.avi"))

        self.video_widget = QVideoWidget(self)
        self.media_player.setVideoOutput(self.video_widget)
        self.video_widget.move(0, 0)

        self.a = QPushButton(self)
        self.a.clicked.connect(self.b)
        self.a.move(100, 100)

    def b(self):
        self.media_player.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VideoPlayer()
    ex.show()
    sys.exit(app.exec())