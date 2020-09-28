from typing import List, Optional

from qtpy import QtCore, QtGui

from prettyqt import gui, core, widgets
from prettyqt.utils import colors


TEXT_COLOR = gui.Color("lightgray")
BACKGROUND_COLOR = gui.Color("dimgrey")
PEN_COLOR = "cyan"
FONT = gui.Font("Decorative", 10)


class VideoSample:
    def __init__(
        self,
        duration: int,
        color: colors.ColorType = "yellow",
        picture: Optional[QtGui.QPixmap] = None,
    ):
        self.duration = duration
        self.color = colors.get_color(color)  # Floating color
        self.def_color = colors.get_color(color)  # DefaultColor
        self.picture = None if picture is None else picture.scaledToHeight(45)
        self.start_pos = 0  # Initial position
        self.end_pos = self.duration  # End position


class Timeline(widgets.Widget):

    position_changed = core.Signal(int)
    selection_changed = core.Signal(VideoSample)

    def __init__(self, duration: int, length: int):
        super().__init__()
        self.set_title("Timeline")
        self.duration = duration
        self.length = length

        # Set variables
        self.set_background_color(BACKGROUND_COLOR)
        self.set_text_color(TEXT_COLOR)
        self.set_text_font(FONT)
        self.pos = None
        self.pointer_pos = None
        self.pointer_time_pos = None
        self.selected_sample = None
        self.clicking = False  # Check if mouse left button is being pressed
        self.is_in = False  # check if user is in the widget
        self.video_samples: List[VideoSample] = []  # List of video samples
        self.setMouseTracking(True)  # Mouse events
        self.setAutoFillBackground(True)  # background
        self.setGeometry(300, 300, self.length, 200)

        # Set Background
        pal = gui.Palette()
        pal.set_color("background", self.background_color)
        self.setPalette(pal)

    def __len__(self):
        return len(self.video_samples)

    def __getitem__(self, index: int):
        return self.video_samples[index]

    def __setitem__(self, index: int, value: VideoSample):
        self.video_samples[index] = value

    def __add__(self, other: VideoSample):
        if isinstance(other, (VideoSample)):
            self.add(other)
            return self

    def add_sample(
        self,
        duration: int,
        color: colors.ColorType = "yellow",
        picture: Optional[QtGui.QPixmap] = None,
    ) -> VideoSample:
        sample = VideoSample(duration, color, picture)
        self.add(sample)
        return sample

    def add(self, sample: VideoSample):
        self.video_samples.append(sample)

    def paintEvent(self, event):
        qp = gui.Painter()
        w = 0
        # Draw time
        scale = self.get_scale()
        with qp.paint_on(self):
            qp.set_color(self.text_color)
            qp.setFont(self.font)
            qp.use_antialiasing()
            while w <= self.width():
                time_string = self.get_time_string(w * scale)
                qp.drawText(w - 50, 0, 100, 100, QtCore.Qt.AlignHCenter, time_string)
                w += 100
            # Draw down line
            qp.set_pen(color=PEN_COLOR, width=5)
            qp.drawLine(0, 40, self.width(), 40)

            # Draw dash lines
            point = 0
            qp.set_pen(color=self.text_color)
            qp.drawLine(0, 40, self.width(), 40)
            while point <= self.width():
                y2 = 30 if point % 30 != 0 else 20
                qp.drawLine(3 * point, 40, 3 * point, y2)
                point += 10

            if self.pos is not None and self.is_in:
                qp.drawLine(self.pos.x(), 0, self.pos.x(), 40)

            poly = gui.Polygon()
            if self.pointer_pos is not None:
                val = self.pointer_time_pos / self.get_scale()
                line = core.Line(val, 40, val, self.height())
                poly.add_points((val - 10, 20), (val + 10, 20), (val, 40))
            else:
                line = core.Line(0, 0, 0, self.height())
                poly.add_points((-10, 20), (10, 20), (0, 40))

            # Draw samples
            t = 0
            for sample in self.video_samples:
                scaled_dur = sample.duration / scale
                scaled_t = t / scale
                t += sample.duration
                # Clear clip path
                with qp.clip_path() as path:
                    rect = core.RectF(scaled_t, 50, scaled_dur, 200)
                    path.addRoundedRect(rect, 10, 10)

                # Draw sample
                path = gui.PainterPath()
                qp.set_pen(color=sample.color)
                rect = core.RectF(scaled_t, 50, scaled_dur, 50)
                path.addRoundedRect(rect, 10, 10)
                sample.start_pos = scaled_t
                sample.end_pos = scaled_t + scaled_dur
                qp.fillPath(path, sample.color)
                qp.drawPath(path)

                # Draw preview pictures
                if sample.picture is None:
                    continue
                pic_width = sample.picture.size().width()
                if pic_width < scaled_dur:
                    width = pic_width
                    pic = sample.picture
                else:
                    width = scaled_dur
                    pic = sample.picture.copy(0, 0, scaled_dur, 45)
                with qp.clip_path() as path:
                    rect = core.RectF(scaled_t, 52.5, width, 45)
                    path.addRoundedRect(rect, 10, 10)
                rect = core.Rect(scaled_t, 52.5, width, 45)
                qp.drawPixmap(rect, pic)

            # Clear clip path
            with qp.clip_path() as path:
                path.add_rect(self.rect())

            # Draw pointer
            qp.set_color(PEN_COLOR)
            qp.set_brush(PEN_COLOR)

            qp.drawPolygon(poly)
            qp.drawLine(line)

    def mouseMoveEvent(self, e):
        self.pos = e.pos()

        # if mouse is being pressed, update pointer
        if self.clicking:
            x = self.pos.x()
            self.pointer_pos = x
            self.position_changed.emit(x)
            self._check_selection(x)
            self.pointer_time_pos = self.pointer_pos * self.get_scale()

        self.update()

    def mousePressEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            x = e.pos().x()
            self.pointer_pos = x
            self.position_changed.emit(x)
            self.pointer_time_pos = self.pointer_pos * self.get_scale()

            self._check_selection(x)

            self.update()
            self.clicking = True  # Set clicking check to true

    def mouseReleaseEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            self.clicking = False  # Set clicking check to false

    def enterEvent(self, e):
        self.is_in = True

    def leaveEvent(self, e):
        self.is_in = False
        self.update()

    def _check_selection(self, x: int):
        # Check if user clicked in video sample
        for sample in self.video_samples:
            if sample.start_pos < x < sample.end_pos:
                sample.color = gui.Color(PEN_COLOR)
                if self.selected_sample is not sample:
                    self.selected_sample = sample
                    self.selection_changed.emit(sample)
            else:
                sample.color = sample.def_color

    def get_time_string(self, seconds: int) -> str:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)

    def get_scale(self) -> float:
        return float(self.duration) / float(self.width())

    def set_background_color(self, color: colors.ColorType):
        color = colors.get_color(color)
        self.background_color = color

    def set_text_color(self, color: colors.ColorType):
        color = colors.get_color(color)
        self.text_color = color

    def set_text_font(self, font: gui.Font):
        self.font = font


if __name__ == "__main__":
    app = widgets.app()
    tl = Timeline(60, 60)
    icon = gui.icon.get_icon("mdi.folder")
    px = icon.pixmap(256, 256)
    sample = VideoSample(20, picture=px)
    tl += sample
    tl.show()
    app.main_loop()
