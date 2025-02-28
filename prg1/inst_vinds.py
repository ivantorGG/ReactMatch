import sys

from PyQt5.QtCore import QUrl, QFileInfo, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QCoreApplication


class GoInstructions(QMainWindow):
    def __init__(self, video, video_lenth, delete_volume=False):
        super().__init__()
        self.setWindowTitle('Смотри, не отвлекайся')
        self.video = video
        self.video_lenth = video_lenth
        self.delete_volume = delete_volume
        self.initUI()
        self.resize(1000, 750)
        self.move(450, 125)

    def initUI(self):
        self.seconds = 0
        player = QMediaPlayer(self)
        video_widget = QVideoWidget(self)
        file_info = QFileInfo(self.video)
        url = QUrl.fromLocalFile(file_info.absoluteFilePath())
        player.setMedia(QMediaContent(url))
        player.setVideoOutput(video_widget)
        video_widget.resize(1000, 750)
        if self.delete_volume:
            player.setVolume(0)
        player.play()
        self.close_tmr = QTimer()
        self.close_tmr.start(1000)
        self.close_tmr.timeout.connect(self.close_vind_func)

    def close_vind_func(self):
        self.seconds += 1
        if self.seconds >= self.video_lenth:
            QCoreApplication.instance().quit()


if __name__ == '__main__':
    app = QApplication([])
    ex = GoInstructions('first_vid.avi', 10, False)
    ex.show()
    sys.exit(app.exec())
