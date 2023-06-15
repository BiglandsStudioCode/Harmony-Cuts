import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QRadioButton, QMessageBox, QInputDialog, QDialog, QFormLayout
from PyQt5.QtCore import Qt


class ProjectView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Harmony Cuts")
        self.setGeometry(100, 100, 800, 600)

        # Main widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Layouts
        main_layout = QVBoxLayout(main_widget)
        project_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # Project list
        self.project_list = QListWidget(self)
        project_layout.addWidget(self.project_list)

        # Buttons
        create_button = QPushButton("Create Project", self)
        open_button = QPushButton("Open Project", self)
        delete_button = QPushButton("Delete Project", self)
        settings_button = QPushButton("Settings", self)
        button_layout.addWidget(create_button)
        button_layout.addWidget(open_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(settings_button)

        # Connect button signals to slots
        create_button.clicked.connect(self.create_project)
        open_button.clicked.connect(self.open_project)
        delete_button.clicked.connect(self.delete_project)
        settings_button.clicked.connect(self.open_settings)

        # Add layouts to main layout
        main_layout.addLayout(project_layout)
        main_layout.addLayout(button_layout)

        # Look for existing projects
        self.populate_project_list()

        # Check and set theme
        self.dark_theme = self.check_theme()
        self.set_theme()

    def populate_project_list(self):
        projects_folder = "Projects"
        if not os.path.exists(projects_folder):
            os.makedirs(projects_folder)

        projects = os.listdir(projects_folder)
        self.project_list.clear()
        self.project_list.addItems(projects)

    def create_project(self):
        project_name, ok = QInputDialog.getText(self, "Create Project", "Enter project name:")
        if ok and project_name:
            # Create project folder
            project_folder = os.path.join("Projects", project_name)
            os.makedirs(project_folder, exist_ok=True)

            # Add project to the list
            self.project_list.addItem(project_name)

    def open_project(self):
        selected_project = self.project_list.currentItem()
        if selected_project:
            QMessageBox.information(self, "Open Project", f"Opening project: {selected_project.text()}")

    def delete_project(self):
        selected_project = self.project_list.currentItem()
        if selected_project:
            reply = QMessageBox.question(self, "Delete Project", f"Do you want to delete project: {selected_project.text()}?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                # Remove project folder
                project_folder = os.path.join("Projects", selected_project.text())
                os.rmdir(project_folder)

                # Remove project from the list
                self.project_list.takeItem(self.project_list.currentRow())

    def check_theme(self):
        theme_file = os.path.join("settings", "theme.txt")
        if os.path.exists(theme_file):
            with open(theme_file, "r") as file:
                theme = file.read().strip()
                return theme.lower() == "dark"
        return True

    def set_theme(self):
        if self.dark_theme:
            self.setStyleSheet("background-color: #303030; color: #ffffff;")
        else:
            self.setStyleSheet("background-color: #ffffff; color: #000000;")

    def toggle_theme(self):
        self.dark_theme = not self.dark_theme
        self.set_theme()
        self.set_theme_button_text()

    def set_theme_button_text(self):
        if self.dark_theme:
            self.settings_window.theme_button.setText("Turn on Light Theme")
        else:
            self.settings_window.theme_button.setText("Turn on Dark Theme")

    def open_settings(self):
        self.settings_window = SettingsWindow(self.dark_theme)
        self.settings_window.theme_button.clicked.connect(self.toggle_theme)
        self.settings_window.exec_()

    def closeEvent(self, event):
        event.ignore()
        reply = QMessageBox.question(self, 'Exit Confirmation', "Are you sure you want to exit Harmony Cuts?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class SettingsWindow(QDialog):
    def __init__(self, dark_theme):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(300, 200)

        self.dark_theme = dark_theme

        layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        self.theme_button = QPushButton()
        form_layout.addRow("Theme:", self.theme_button)

        layout.addLayout(form_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    project_view = ProjectView()
    project_view.show()
    sys.exit(app.exec())
