import sys

from PySide2.QtWidgets import QApplication

sys.path.append(".")

from src.picbedshower.picbedshower import PicBedShower

if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = PicBedShower()
    example.show()
    sys.exit(app.exec_())