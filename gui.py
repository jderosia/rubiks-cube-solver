from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
from typing import List
import cube as c

def main():
    app = QApplication([])
    window = QWidget()
    window.setGeometry(400, 300, 1000, 500)
    window.setWindowTitle("Rubik's Cube Solver")


    # Simple Text
    #
    # label = QLabel(window)
    # label.setText("Rubik's Cube Solver")
    # label.setFont(QFont("Arial", 16))

    layout = QVBoxLayout()

    label = QLabel("Press Button Below")
    button = QPushButton("Press Me!")





    cubeLayout = makeCube()

    cubeWindow = QWidget()
    cubeWindow.setLayout(cubeLayout)






    # layout.addWidget(label)
    # layout.addWidget(pieceDropdown)
    # layout.addWidget(button)
    # layout.addWidget(faceWidget)




    cubeWindow.show()
    app.exec_()

def makePieceDropdown(color: int) -> QComboBox:
    pieceDropdown = QComboBox()
    pieceDropdown.addItem(QIcon("Colors/WhiteSquare.png"), None)
    pieceDropdown.addItem(QIcon("Colors/RedSquare.png"), None)
    pieceDropdown.addItem(QIcon("Colors/GreenSquare.png"), None)
    pieceDropdown.addItem(QIcon("Colors/OrangeSquare.png"), None)
    pieceDropdown.addItem(QIcon("Colors/BlueSquare.png"), None)
    pieceDropdown.addItem(QIcon("Colors/YellowSquare.png"), None)
    pieceDropdown.setFixedSize(pieceDropdown.sizeHint())
    pieceDropdown.setCurrentIndex(color)
    return pieceDropdown

def makeFace(name: str, color: int) -> QGridLayout:
    faceLayout = QGridLayout()
    label = QLabel()
    label.setText(name)
    label.setFont(QFont("Arial", 16))
    faceLayout.addWidget(label, 0, 1)
    for i in range(3):
        for j in range(3):
            faceLayout.addWidget(makePieceDropdown(color), i + 1, j)
    return faceLayout

def makeCube() -> QGridLayout:
    cubeLayout = QGridLayout()
    cubeLayout.addLayout(makeFace("White", 0), 2, 1)
    colors = ["Blue", "Red", "Green", "Orange"]
    cubeLayout.addLayout(makeFace(colors[0], 4), 1, 0)
    for i in range(3):
        i += 1
        cubeLayout.addLayout(makeFace(colors[i], i), 1, i)
    cubeLayout.addLayout(makeFace("Yellow", 5), 0, 1)
    button = QPushButton("Solve Cube")
    button.clicked.connect(lambda: on_clicked(cubeLayout))
    cubeLayout.addWidget(button, 2, 3)
    return cubeLayout

def getPieceIndex(item: QLayoutItem) -> int:
    dropdown = item.widget()
    return dropdown.currentIndex()

def getFaceIndices(face: QLayoutItem) -> List[int]:

    faceColors: List[int] = []
    for i in range(3):
        for j in range(3):
            index = getPieceIndex(face.itemAtPosition(i + 1, j))
            faceColors.append(index)
    return faceColors

def getCubeIndices(cube: QLayoutItem) -> List[List[int]]:

    cubeColors: List[List[int]] = []

    # Bottom
    bottomIndices = getFaceIndices(cube.itemAtPosition(2, 1))
    cubeColors.append(bottomIndices)


    for i in range(4):
        sideIndices = getFaceIndices(cube.itemAtPosition(1, (i + 1) % 4))
        cubeColors.append(sideIndices)


    topIndices = getFaceIndices(cube.itemAtPosition(0, 1))
    cubeColors.append(topIndices)

    return cubeColors

def on_clicked(cube: QGridLayout):

    cubeIndices = getCubeIndices(cube)
    cubeRep = c.Cube()
    ctr = 0
    for i in range(6):
        for j in range(9):
            cubeRep.cube[i][j] = c.Color(cubeIndices[i][j])
            ctr += 1
    cubeRep.solve()






if __name__ == '__main__':
    main()