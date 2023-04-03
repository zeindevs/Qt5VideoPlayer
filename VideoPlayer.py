import os
import sys

from PyQt5.QtCore import (QDir, QPoint, Qt, QTime, QUrl, QCommandLineParser)
from PyQt5.Qt import QIcon, QKeySequence, QMouseEvent, QWheelEvent, QDropEvent, QDragEnterEvent
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMenu, QMainWindow, QSizePolicy, QStyle, QVBoxLayout, QWidget, QShortcut, QMessageBox)


from ui.Ui_videocontrol import Ui_VideoControl
# from ui.Ui_videoplayer import Ui_VideoPlayer


basedir = os.path.dirname(__file__)


class VideoControl(QWidget, Ui_VideoControl):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.mediaPlayer: QMediaPlayer = QMediaPlayer()

        self.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setContentsMargins(6, 0, 6, 6)

        self.playButton.setEnabled(False)
        self.playButton.setText("")
        self.playButton.setIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.setSingleStep(2)
        self.positionSlider.setPageStep(20)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.labelPosition.setUpdatesEnabled(True)
        self.labelDuration.setUpdatesEnabled(True)

    def setMediaPlayer(self, mediaPlayer: QMediaPlayer):
        self.mediaPlayer = mediaPlayer

    def toggleSlider(self, toggle=None):
        if toggle:
            self.show()
            return
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def forwardSlider(self, value: int = 50):
        print("Forward")
        self.mediaPlayer.setPosition(
            self.mediaPlayer.position() + value*60)

    def backSlider(self, value: int = 50):
        print("backward")
        self.mediaPlayer.setPosition(
            self.mediaPlayer.position() - value*60)

    def volumeUp(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() + 5)
        print("Volume: " + str(self.mediaPlayer.volume()))

    def volumeDown(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() - 5)
        print("Volume: " + str(self.mediaPlayer.volume()))

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.State.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state: QMediaPlayer.State):
        if self.mediaPlayer.state() == QMediaPlayer.State.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(
                QStyle.StandardPixmap.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(
                QStyle.StandardPixmap.SP_MediaPlay))

        if self.mediaPlayer.state() == QMediaPlayer.State.StoppedState:
            self.toggleSlider(True)

    def positionChanged(self, position):
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(self.mediaPlayer.position())
        self.labelPosition.setText(mtime.toString())
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(self.mediaPlayer.duration())
        self.labelDuration.setText(mtime.toString())
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(position)
        self.labelPosition.setText(mtime.toString())
        self.mediaPlayer.setPosition(position)


class VideoPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # VARIABLES
        self.widescreen = True
        self.myurl = ""
        self.myinfo = "©2023 Zein Studio\n\nMouse Wheel = Zoom\nUP = Volume Up\nDOWN = Volume Down\n" + \
            "LEFT = < 1 Minute\nRIGHT = > 1 Minute\n" + \
            "SHIFT+LEFT = < 10 Minutes\nSHIFT+RIGHT = > 10 Minutes"

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.Flag.VideoSurface)
        self.mediaPlayer.setVolume(100)

        self.videoPlayer = QVideoWidget()
        self.videoPlayer.setSizePolicy(QSizePolicy.Policy.Expanding,
                                       QSizePolicy.Policy.Expanding)
        self.videoControl = VideoControl()
        self.videoControl.setMediaPlayer(self.mediaPlayer)
        self.mediaPlayer.setVideoOutput(self.videoPlayer)

        self.mediaPlayer.mediaStatusChanged.connect(self.printMediaData)
        self.mediaPlayer.stateChanged.connect(
            self.videoControl.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(
            self.videoControl.positionChanged)
        self.mediaPlayer.durationChanged.connect(
            self.videoControl.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.videoPlayer)
        layout.addWidget(self.videoControl)

        self.setLayout(layout)

        # SHORTCUTS
        self.shortcut = QShortcut(QKeySequence("q"), self)
        self.shortcut.activated.connect(self.handlet)

        self.shortcut = QShortcut(QKeySequence("o"), self)
        self.shortcut.activated.connect(self.openFile)

        self.shortcut = QShortcut(QKeySequence(" "), self)
        self.shortcut.activated.connect(self.videoControl.play)

        self.shortcut = QShortcut(QKeySequence("f"), self)
        self.shortcut.activated.connect(self.handleFullscreen)

        self.shortcut = QShortcut(QKeySequence("m"), self)
        self.shortcut.activated.connect(self.handleMaximized)

        self.shortcut = QShortcut(QKeySequence("i"), self)
        self.shortcut.activated.connect(self.handleInfo)

        self.shortcut = QShortcut(QKeySequence("s"), self)
        self.shortcut.activated.connect(self.videoControl.toggleSlider)

        self.shortcut = QShortcut(QKeySequence(Qt.Key.Key_Right), self)
        self.shortcut.activated.connect(self.videoControl.forwardSlider)

        self.shortcut = QShortcut(QKeySequence(Qt.Key.Key_Left), self)
        self.shortcut.activated.connect(self.videoControl.backSlider)

        self.shortcut = QShortcut(QKeySequence(
            Qt.KeyboardModifier.ShiftModifier + Qt.Key.Key_Right), self)
        self.shortcut.activated.connect(
            lambda: self.videoControl.forwardSlider(100))
        self.shortcut = QShortcut(QKeySequence(
            Qt.KeyboardModifier.ShiftModifier + Qt.Key.Key_Left), self)
        self.shortcut.activated.connect(
            lambda: self.videoControl.backSlider(100))

        self.shortcut = QShortcut(QKeySequence(Qt.Key.Key_Up), self)
        self.shortcut.activated.connect(self.videoControl.volumeUp)

        self.shortcut = QShortcut(QKeySequence(Qt.Key.Key_Down), self)
        self.shortcut.activated.connect(self.videoControl.volumeDown)

        print("Qt5 Player started")
        print("press 'o' to open file (see context menu for more)")

    def contextMenuRequested(self, point: QPoint):
        menu = QMenu()
        actionFile = menu.addAction(QIcon.fromTheme(
            "video-x-generic"), "Open File (o)")
        menu.addSeparator()
        actionToggle = menu.addAction(
            QIcon.fromTheme("next"), "Show / Hide Slider (s)")
        actionFull = menu.addAction(QIcon.fromTheme(
            "view-fullscreen"), "Fullscreen (f)")
        action169 = menu.addAction(QIcon.fromTheme("tv-symbolic"), "16 : 9")
        action43 = menu.addAction(QIcon.fromTheme("tv-symbolic"), "4 : 3")
        menu.addSeparator()
        actionInfo = menu.addAction(QIcon.fromTheme("help-about"), "Info (i)")
        menu.addSeparator()
        actiont = menu.addAction(
            QIcon.fromTheme("application-exit"), "Exit (q)")

        actionFile.triggered.connect(self.openFile)
        actiont.triggered.connect(self.handleQuit)
        actionFull.triggered.connect(self.handleFullscreen)
        actionInfo.triggered.connect(self.handleInfo)
        actionToggle.triggered.connect(self.videoControl.toggleSlider)
        action169.triggered.connect(self.screen169)
        action43.triggered.connect(self.screen43)
        menu.exec_(self.mapToGlobal(point))

    def handlet(self):
        self.mediaPlayer.stop()
        print("Goodbye ...")
        app.exit()

    def handleFullscreen(self):
        if self.windowState() & Qt.WindowState.WindowFullScreen:
            QApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)
            self.showNormal()
            print("no Fullscreen")
        else:
            self.showFullScreen()
            print("Fullscreen entered")

    def handleMaximized(self):
        if self.windowState() & Qt.WindowState.WindowMaximized:
            QApplication.setOverrideCursor(Qt.CursorShape.ArrowCursor)
            self.showNormal()
            print("no Maximized")
        else:
            self.showMaximized()
            print("Maximized entered")

    def screen169(self):
        self.widescreen = True
        mwidth = self.frameGeometry().width()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mratio = 1.778
        self.setGeometry(mleft, mtop, mwidth, round(mwidth / mratio))

    def screen43(self):
        self.widescreen = False
        mwidth = self.frameGeometry().width()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mratio = 1.33
        self.setGeometry(mleft, mtop, mwidth, round(mwidth / mratio))

    def handleInfo(self):
        msg = QMessageBox()
        msg.about(self, "Qt5 Player", self.myinfo)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        self.handleFullscreen()

    def mousePressEvent(self, event: QMouseEvent):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.windowState() != Qt.WindowState.WindowFullScreen:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def wheelEvent(self, event: QWheelEvent):
        mwidth = self.frameGeometry().width()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mscale = round(event.angleDelta().y() / 5)
        if self.widescreen and self.windowState() != Qt.WindowState.WindowFullScreen:
            if mscale <= 0:
                self.setGeometry(mleft, mtop + 24, mwidth + mscale,
                                 round((mwidth + mscale) / 1.778))
            else:
                self.setGeometry(mleft, mtop + mscale, mwidth + mscale,
                                 round((mwidth + mscale) / 1.778))

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open Movie", QDir.homePath() + "/Videos", "Media (*.webm *.mp4 *.ts *.avi *.mpeg *.mpg *.mkv *.VOB *.m4v *.3gp *.mp3 *.m4a *.wav *.ogg *.flac *.m3u *.m3u8)")

        if filename != '':
            self.loadFilm(filename)
            print("File loaded")

    def loadFilm(self, filename: str):
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
        self.videoControl.playButton.setEnabled(True)
        self.mediaPlayer.play()

    def exitCall(self):
        sys.exit(app.exec_())

    def handleError(self):
        self.videoControl.playButton.setEnabled(False)
        # QMessageBox.warning(self, 'Error', self.mediaPlayer.errorString())
        # self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

    def dataReady(self):
        pass

    def playFromURL(self):
        pass

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        print("Drop")
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0].toString()
            print("url: ", url)
            self.mediaPlayer.stop()
            self.mediaPlayer.setMedia(QMediaContent(QUrl(url)))
            self.videoControl.playButton.setDisabled(False)
            self.mediaPlayer.play()

    def printMediaData(self):
        if self.mediaPlayer.mediaStatus() == 6:
            if self.mediaPlayer.isMetaDataAvailable() and not self.isFullScreen() or not self.isMaximized() == False:
                if self.mediaPlayer.metaData("Resolution"):
                    res = str(self.mediaPlayer.metaData("Resolution")).partition(
                        "PyQt5.QtCore.QSize(")[2].replace(", ", "x").replace(")", "")
                    print("%s%s" % ("Video Resolution = ", res))
                    # if int(res.partition("x")[0]) / int(res.partition("x")[2]) < 1.5:
                    #     self.screen43()
                    # else:
                    #     self.screen169()
            else:
                print("no metaData available")


class MainWindow(QMainWindow):
    def __init__(self, args):
        super().__init__(args)

        videoPlayer = VideoPlayer()

        self.setCentralWidget(videoPlayer)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    parser = QCommandLineParser()
    parser.addPositionalArgument('file', QApplication.translate('main', 'The file to open'))
    parser.process(app)

    player = VideoPlayer()
    app.setStyle('Fusion')
    player.setAcceptDrops(True)
    player.setWindowTitle("Qt5 Video Player")
    player.setWindowIcon(QIcon('logo.png'))
    player.setWindowFlags(Qt.WindowType.Window)
    player.setGeometry(100, 200, 720, 360)
    player.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    player.customContextMenuRequested[QPoint].connect(
        player.contextMenuRequested)
    player.show()

    if len(parser.positionalArguments()) > 0:
        filename = parser.positionalArguments()
        print("file: %s" % filename[0])
        player.loadFilm(filename[0])
    sys.exit(app.exec_())
