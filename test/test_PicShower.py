import sys
from PySide2.QtGui import QBrush, QColor, QPaintEvent, QPainter, QPixmap

from PySide2.QtWidgets import QApplication, QLabel
import requests

sys.path.append(".")

from src.picbedshower.picshower import PicShower


if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = PicShower("tmp")
    example.show()
    sys.exit(app.exec_())

# if __name__ == '__main__':
#     r = requests.get('https://pandao.github.io/editor.md/images/logos/editormd-logo-180x180.png')
#     with open("./tmp/pic.png", 'wb') as fd:
#         for chunk in r.iter_content(10):
#             fd.write(chunk)