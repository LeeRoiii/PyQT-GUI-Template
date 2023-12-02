import sys
from PyQt5.QtCore import Qt, QSize, QEvent
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen, QKeySequence
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QGraphicsDropShadowEffect, QHBoxLayout, QLabel, QSizeGrip,
    QSpacerItem, QMessageBox, QSizePolicy, QShortcut, QStackedWidget
)
import qtawesome as qta


class Template(QWidget):

    def __init__(self):
        super().__init__()
        # Initialize variables for window dragging and resizing
        self.drag_position = None
        self.handle_size = 10
        self.resize_handle = QSizeGrip(self)
        self.draggable = True
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.titleBarHeight = 30
        self.current_page = 0
        self.mousePressAction = None
        self.resizeEdgeMargin = 10
        self.setMouseTracking(True)
        self.installEventFilter(self)
        self.stacked_widget = QStackedWidget(self)

        # Set up the main window
        self.setup_main_page()
        self.setup_next_page()
        self._setup_main_window()
        self._setup_title_bar()
        self._setup_content()
        self.button_common_style = ""

    def _setup_main_window(self):
        """Configure main window properties."""
        self.setMinimumSize(850, 650)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 850, 650)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # Drop shadow effect for the main window
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(40)
        shadow_effect.setXOffset(0)
        shadow_effect.setYOffset(5)
        shadow_effect.setColor(QColor(0, 0, 0, 30))
        self.setGraphicsEffect(shadow_effect)

    def _setup_title_bar(self):
        """Configure the title bar with title and control buttons."""
        title_container = QHBoxLayout()
        title_container.setContentsMargins(10, 10, 10, 0)

        # Styling and layout for the header/title bar
        self.header_widget = QWidget()
        header_bg_color = "rgb(255, 255, 255, 220)"
        header_border_color = "rgba(255, 255, 255, 50)"
        header_style = f"""
        background-color: {header_bg_color};
        border: 1px solid {header_border_color};
        border-radius: 10px;
        """
        self.header_widget.setStyleSheet(header_style)
        header_layout = QHBoxLayout(self.header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)

        self._setup_buttons()

        # Icon and title for the header
        header_icon = qta.icon('fa.heart', color='#191919')
        icon_label = QLabel()
        icon_label.setPixmap(header_icon.pixmap(QSize(24, 24)))
        header_title = QLabel("Template")
        header_title.setStyleSheet(
            "font-family: 'Concord'; font-size: 18px; font-weight: bold; color: #191919; margin-left: 0px; margin-right: 0px;")

        # First add the icon and title to the header_layout
        header_layout.addWidget(icon_label)
        header_layout.addWidget(header_title, alignment=Qt.AlignLeft)

        # Then add a spacer to push the control buttons to the right
        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        header_layout.addSpacerItem(spacer)

        header_layout.addLayout(self.title_bar)
        title_container.addWidget(self.header_widget)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(title_container)

    def _setup_buttons(self):
        """Configure control buttons for the title bar."""
        self.button_common_style = """
            QPushButton {
                background-color: rgba(255, 255, 255, 230);
                border: none;
                border-radius: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(220, 220, 220, 230);
            }
        """

        # Close button
        self.close_btn = QPushButton()
        self.close_btn.setIcon(qta.icon('fa.times', color='#191919'))
        self.close_btn.setStyleSheet(self.button_common_style)
        self.close_btn.setIconSize(QSize(16, 16))
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.clicked.connect(self.close)

        # Minimize button
        self.minimize_btn = QPushButton()
        self.minimize_btn.setIcon(qta.icon('fa.minus', color='#191919'))
        self.minimize_btn.setStyleSheet(self.button_common_style)
        self.minimize_btn.setIconSize(QSize(16, 16))
        self.minimize_btn.setFixedSize(24, 24)
        self.minimize_btn.clicked.connect(self.ToggleMinimized)

        # Maximize button
        self.maximize_btn = QPushButton()
        self.maximize_btn.setIcon(qta.icon('fa.square-o', color='#191919'))
        self.maximize_btn.setStyleSheet(self.button_common_style)
        self.maximize_btn.setIconSize(QSize(16, 16))
        self.maximize_btn.setFixedSize(24, 24)
        self.maximize_btn.clicked.connect(self.toggle_maximize)

        # Previous button
        self.prev_btn = QPushButton()
        self.prev_btn.setIcon(qta.icon('fa.arrow-left', color='#191919'))
        self.prev_btn.setStyleSheet(self.button_common_style)
        self.prev_btn.setIconSize(QSize(16, 16))
        self.prev_btn.setFixedSize(24, 24)
        self.prev_btn.clicked.connect(self.navigate_previous_tab)

        # Next button
        self.next_btn = QPushButton()
        self.next_btn.setIcon(qta.icon('fa.arrow-right', color='#191919'))
        self.next_btn.setStyleSheet(self.button_common_style)
        self.next_btn.setIconSize(QSize(16, 16))
        self.next_btn.setFixedSize(24, 24)
        self.next_btn.clicked.connect(self.navigate_next_tab)

        # Title bar layout
        self.title_bar = QHBoxLayout()
        self.title_bar.setSpacing(5)

        # Add buttons to the title bar
        self.title_bar.addWidget(self.prev_btn)
        self.title_bar.addWidget(self.next_btn)
        self.title_bar.addWidget(self.minimize_btn)
        self.title_bar.addWidget(self.maximize_btn)
        self.title_bar.addWidget(self.close_btn)

    def setup_main_page(self):
        """Set up the content for the main page."""
        main_page = QWidget()

        # Add placeholder label with text
        placeholder_label = QLabel("Main Page Content Goes Here")
        placeholder_label.setAlignment(Qt.AlignCenter)
        placeholder_label.setStyleSheet("font-size: 16px; color: #555;")

        # Example: Adding other widgets or designs as needed

        # Set up layout
        layout = QVBoxLayout(main_page)
        layout.addWidget(placeholder_label)
        # Add more widgets or designs to the layout as needed

        print('Main page')
        return main_page

    def setup_next_page(self):
        """Set up the content for the graph page."""
        next_page = QWidget()

        # Add placeholder label with text
        placeholder_label = QLabel("Next Page Content Goes Here")
        placeholder_label.setAlignment(Qt.AlignCenter)
        placeholder_label.setStyleSheet("font-size: 16px; color: #555;")

        # Example: Adding a chart or graph widget
        # placeholder_chart = YourChartWidget()

        # Example: Adding other widgets or designs as needed

        # Set up layout
        layout = QVBoxLayout(next_page)
        layout.addWidget(placeholder_label)
        # layout.addWidget(placeholder_chart)
        # Add more widgets or designs to the layout as needed

        return next_page

    def _setup_content(self):
        """Set up the main content of the window using QStackedWidget."""
        self.content_pages = QStackedWidget(self)
        self.main_layout.addWidget(self.content_pages)

        # Add main and graph pages to the QStackedWidget
        self.content_pages.addWidget(self.setup_main_page())
        self.content_pages.addWidget(self.setup_next_page())


    def navigate_previous_tab(self):
        """Navigate to the previous page in the QStackedWidget."""
        self.current_page -= 1
        self.content_pages.setCurrentIndex(self.current_page)

    def navigate_next_tab(self):
        """Navigate to the next page in the QStackedWidget."""
        self.current_page += 1
        self.content_pages.setCurrentIndex(self.current_page)
        # Call the method to refresh data for all charts

    def ToggleMinimized(self):
        """Toggle between normal and minimized window states."""
        if self.isMinimized():
            self.showNormal()
        else:
            self.showMinimized()

    def toggle_maximize(self):
        """Toggle between maximized and normal window states."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mousePressEvent(self, event):
        """Handle mouse press event to initiate window dragging."""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos()

    def mouseMoveEvent(self, event):
        """Handle mouse move event to move the window."""
        if self.drag_position is not None:
            self.move(self.pos() + event.globalPos() - self.drag_position)
            self.drag_position = event.globalPos()

    def resizeEvent(self, event):
        """Handle window resize event."""
        super().resizeEvent(event)
        self.resize_handle.setGeometry(self.width() - self.handle_size, self.height() - self.handle_size,
                                      self.handle_size, self.handle_size)

    def paintEvent(self, event):
        """Customize the appearance of the window."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.NoPen))
        painter.setBrush(QBrush(QColor(255, 255, 255, 230)))
        painter.drawRoundedRect(10, 10, self.width() - 20, self.height() - 20, 20, 20)

    def mouseReleaseEvent(self, event):
        """Handle mouse release event to reset drag_position."""
        if event.button() == Qt.LeftButton:
            self.drag_position = None

    def updateCursor(self, event):
        """Update the mouse cursor based on its position."""
        mouseX = event.pos().x()
        mouseY = event.pos().y()
        x, y, w, h = self.geometry().getRect()

        if mouseX < self.resizeEdgeMargin:
            if mouseY < self.resizeEdgeMargin:
                self.setCursor(Qt.SizeFDiagCursor)
            elif mouseY > h - self.resizeEdgeMargin:
                self.setCursor(Qt.SizeBDiagCursor)
            else:
                self.setCursor(Qt.SizeHorCursor)
        elif mouseX > w - self.resizeEdgeMargin:
            if mouseY < self.resizeEdgeMargin:
                self.setCursor(Qt.SizeBDiagCursor)
            elif mouseY > h - self.resizeEdgeMargin:
                self.setCursor(Qt.SizeFDiagCursor)
            else:
                self.setCursor(Qt.SizeHorCursor)
        elif mouseY < self.resizeEdgeMargin or mouseY > h - self.resizeEdgeMargin:
            self.setCursor(Qt.SizeVerCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def eventFilter(self, obj, event):
        """Event filter to handle custom event processing."""
        if event.type() == QEvent.MouseMove:
            self.updateCursor(event)
        return super().eventFilter(obj, event)

    def closeEvent(self, event):
        """Override the close event to show a custom dialog."""
        confirmation = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to exit the application?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    try:
        QApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)
        app = QApplication(sys.argv)
        window = Template()
        window.show()

        close_shortcut = QShortcut(QKeySequence("Ctrl+Q"), window)
        close_shortcut.activated.connect(window.close)

        sys.exit(app.exec_())
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
