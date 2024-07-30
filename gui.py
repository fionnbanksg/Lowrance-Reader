import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QLabel, QSlider, QFileDialog, QMessageBox, QStatusBar
)
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import numpy as np
from reader import read_sl, read_bin
import file_management  # Import the file management functions

class SLViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lowrance SL File Reader")
        self.setGeometry(100, 100, 800, 600)

        self.primary_np = None
        self.dataframe = None
        self.df_primary = None

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.figure = Figure(figsize=(7, 7), dpi=120)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout.addWidget(self.canvas)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.layout.addWidget(self.toolbar)
        self.color_profile_combo = QComboBox()
        self.color_profile_combo.addItems([
            "viridis", "cividis", "plasma", "magma", "inferno", "twilight", 
            "spring", "summer", "autumn", "winter"
        ])
        self.color_profile_combo.currentTextChanged.connect(self.update_image)

        self.intensity_slider = QSlider(Qt.Horizontal)
        self.intensity_slider.setMinimum(0)
        self.intensity_slider.setMaximum(50)
        self.intensity_slider.setValue(10)
        self.intensity_slider.setSingleStep(1)
        self.intensity_slider.setTickInterval(1)
        self.intensity_slider.setTickPosition(QSlider.TicksBelow)
        self.intensity_slider.valueChanged.connect(self.update_image)

        self.layout.addWidget(self.canvas)
        self.layout.addWidget(QLabel("Color Profile:"))
        self.layout.addWidget(self.color_profile_combo)
        self.layout.addWidget(QLabel("Intensity:"))
        self.layout.addWidget(self.intensity_slider)

        self.create_menu()
        
        # Create a status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Initialize the image display
        self.update_image()

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        open_action = file_menu.addAction("Open SL File")
        open_action.triggered.connect(self.open_sl_file)

        export_menu = menu_bar.addMenu("Export")
        export_sonar_action = export_menu.addAction("Export Sonar Data")
        export_sonar_action.triggered.connect(self.handle_export_sonar_data)
        export_other_action = export_menu.addAction("Export Other Data")
        export_other_action.triggered.connect(self.handle_export_other_data)
        process_data_action = export_menu.addAction("Process Data")
        process_data_action.triggered.connect(self.handle_process_data)

    def open_sl_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open SL File", "", "SL files (*.sl3 *.sl2)", options=options
        )
        if file_path:
            print(f"File selected: {file_path}")  # Debug statement
            sl_bin_data = read_bin(file_path)
            df = read_sl(file_path)
            self.dataframe = df
            self.df_primary = df.query("survey_label == 'primary'")
            primary_list = [
                item for f, p in zip(self.df_primary["first_byte"], self.df_primary["frame_size"])
                if (item := np.frombuffer(sl_bin_data[(f+168):(f+(p-168))], dtype="uint8")[:2904]).size == 2904
            ]

            self.primary_np = np.stack(primary_list)
            self.update_image()

    def update_image(self):
        self.ax.clear()
        if self.primary_np is None:
            self.ax.text(
                0.5, 0.5, 'Click File > Open SL File to open an SL2 or SL3 file.',
                horizontalalignment='center', verticalalignment='center',
                transform=self.ax.transAxes, fontsize=12, color='gray'
            )
            self.ax.axis('off')
        else:
            image = self.primary_np.transpose()
            adjusted_image = image * (self.intensity_slider.value() / 10)  # Adjust the intensity scaling
            self.ax.imshow(adjusted_image, cmap=self.color_profile_combo.currentText(), aspect='auto', vmin=0, vmax=255)
            self.ax.axis('off')
        self.ax.set_position([0, 0, 1, 1])
        self.canvas.draw()

    def handle_export_sonar_data(self):
        print("Exporting sonar data...")  # Debug statement
        file_path = file_management.export_sonar_data(self.primary_np, self)
        if file_path:
            self.show_message(f"File saved at: {file_path}")

    def handle_export_other_data(self):
        print("Exporting other data...")  # Debug statement
        file_path = file_management.export_other_data(self.dataframe, self)
        if file_path:
            self.show_message(f"File saved at: {file_path}")

    def handle_process_data(self):
        print("Processing data...")  # Debug statement
        file_path = file_management.process_data(self.primary_np, self)
        if file_path:
            self.show_message(f"File saved at: {file_path}")

    def show_message(self, message):
        print(f"Showing message: {message}")  # Debug statement
        self.status_bar.showMessage(message, 3000)  # Display message for 3 seconds

    def on_mouse_move(self, event):
        if event.inaxes and event.xdata and event.ydata:
            row, col = int(event.ydata), int(event.xdata)
            self.status_bar.showMessage(f"Row: {row}, Column: {col}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SLViewer()
    window.show()
    sys.exit(app.exec_())
