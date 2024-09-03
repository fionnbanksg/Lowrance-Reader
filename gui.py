import sys
import math
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QComboBox, QLabel, QSlider, QFileDialog, QStatusBar, QScrollArea
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from reader import read_sl, read_bin
import file_management
import export_calibrated_data
from colour_profiles.custom_colour import EK500colourmap, EK80colourmap, Hmap  


class SLViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lowrance SL File Reader")
        self.setGeometry(100, 100, 800, 600)

        self.primary_np = None
        self.primary_min_max = None
        self.dataframe = None
        self.df_primary = None
        ("calibration/splines/spline_data_20m.mat")
        self.calibration_data = export_calibrated_data.load_calibration_file("calibration/CALIBRATION.md")
        spline_file = self.calibration_data.get('spline')
        self.spline = export_calibrated_data.load_voltage_spline(spline_file)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)

        self.figure = Figure(figsize=(7, 7), dpi=120)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.scroll_layout.addWidget(self.canvas)
        self.scroll_layout.addWidget(self.toolbar)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)
        
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

        self.color_profile_combo = QComboBox()
        self.color_profile_combo.addItems([
            "cividis", "magma", "twilight", "EK500 Colour Map", "EK80colourmap", "Hmap"
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

        self.layout.addWidget(QLabel("Color Profile:"))
        self.layout.addWidget(self.color_profile_combo)
        self.layout.addWidget(QLabel("Colour Map Dynamic Range:"))
        self.layout.addWidget(self.intensity_slider)

        self.create_menu()

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

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
        process_data_action = export_menu.addAction("Auto Process Data")
        process_data_action.triggered.connect(self.handle_auto_process_data)
        process_data_action = export_menu.addAction("Process Data With Column Selection")
        process_data_action.triggered.connect(self.handle_process_data)
        save_eps_action = export_menu.addAction("Save as EPS")
        save_eps_action.triggered.connect(self.save_as_eps)
        export_as_ts_action = export_menu.addAction("Export Sonar Data as TS")
        export_as_ts_action.triggered.connect(self.handle_export_sonar_data_as_ts)

    def save_as_eps(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Plot as EPS", "", "EPS files (*.eps);;All Files (*)", options=options
        )
        if file_path:
            self.figure.savefig(file_path, format='eps')
            self.show_message(f"Figure saved as EPS at: {file_path}")


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
            print(self.df_primary)
            min_max_list = []
            for index, row in self.df_primary.iterrows():
                min_max_list.append([row['min_range'], row['max_range']])

            # Convert the list to a NumPy array
            self.primary_min_max = np.array(min_max_list)

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
            min_val = self.intensity_slider.value() * 5
            max_val = 255

            cmap_dict = {
                "EK500 Colour Map": EK500colourmap(),
                "EK80colourmap": EK80colourmap(),
                "Hmap": Hmap(),
            }
            cmap = cmap_dict.get(self.color_profile_combo.currentText(), self.color_profile_combo.currentText())

            self.ax.imshow(image, cmap=cmap, aspect='auto', vmin=min_val, vmax=max_val)
            self.ax.axis('off')
        self.ax.set_position([0, 0, 1, 1])
        self.canvas.draw()



    def handle_export_sonar_data(self):
        print("Exporting sonar data...")  # Debug statement
        file_path = file_management.export_sonar_data(self.primary_np, self)
        if file_path:
            self.show_message(f"File saved at: {file_path}")

    def handle_export_sonar_data_as_ts(self):
        print("Exporting sonar data...")  # Debug statement
        file_path = export_calibrated_data.export_ts(self.primary_np, self.primary_min_max, self)
        if file_path:
            self.show_message(f"File saved at: {file_path}")

    def handle_export_other_data(self):
        print("Exporting other data...")  # Debug statement
        file_path = file_management.export_other_data(self.dataframe, self)
        if file_path:
            self.show_message(f"File saved at: {file_path}")

    def handle_auto_process_data(self):
        print("Processing data...")  # Debug statement
        file_path = file_management.process_data(self.primary_np, self)
        if file_path:
            self.show_message(f"File saved at: {file_path}")

    
    def handle_process_data(self):
        print("Processing data...")  # Debug statement
        file_path = file_management.process_data_with_column_selection(self.primary_np, self)
        if file_path:
            self.show_message(f"File saved at: {file_path}")

    def show_message(self, message):
        print(f"Showing message: {message}")  # Debug statement
        self.status_bar.showMessage(message, 3000)  # Display message for 3 seconds

    def on_mouse_move(self, event):
        if not event.inaxes or event.xdata is None or event.ydata is None:
            self.status_bar.clearMessage()
            return

        row, col = int(event.ydata), int(event.xdata)

        if self.primary_min_max is not None and 0 <= col < self.primary_min_max.shape[0]:
            min_range, max_range = self.primary_min_max[col]
            depth_range = max_range - min_range
            depth_at_cursor = row / 3072 * round(depth_range)

            TS = export_calibrated_data.calculate_target_strength_singular(
                row, col, self.calibration_data, self.primary_min_max, self.primary_np, self.spline
            )
            self.status_bar.showMessage(f"Row: {row}, Column: {col}, Depth at cursor: {depth_at_cursor:.2f}m, TS at cursor: {TS:.2f}dB")
        else:
            self.status_bar.clearMessage()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SLViewer()
    window.show()
    sys.exit(app.exec_())