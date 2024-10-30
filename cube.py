from enum import Enum
from typing import List, Dict, Tuple
import copy

class Color(Enum):
    W = 0
    R = 1
    G = 2
    O = 3
    B = 4
    Y = 5

    def __str__(self):
        return self.name

class Cube:

    def __init__(self):
        self.cube: List[List[Color]] = [
            [Color.W, Color.W, Color.W,
             Color.W, Color.W, Color.W,
             Color.W, Color.W, Color.W],
            [Color.R, Color.R, Color.R,
             Color.R, Color.R, Color.R,
             Color.R, Color.R, Color.R],
            [Color.G, Color.G, Color.G,
             Color.G, Color.G, Color.G,
             Color.G, Color.G, Color.G],
            [Color.O, Color.O, Color.O,
             Color.O, Color.O, Color.O,
             Color.O, Color.O, Color.O],
            [Color.B, Color.B, Color.B,
             Color.B, Color.B, Color.B,
             Color.B, Color.B, Color.B],
            [Color.Y, Color.Y, Color.Y,
             Color.Y, Color.Y, Color.Y,
             Color.Y, Color.Y, Color.Y]
            ]

        self.faceDict: Dict[int, str] = {
            0: "Bottom",
            1: "Front",
            2: "Right",
            3: "Back",
            4: "Left",
            5: "Top"
        }

        self.solveAlg: str = ""
        self.scramble: str = ""

    def __str__(self):
        cubeStr = ""
        for i in range(6):
            cubeStr += self.strFace(i)
        return cubeStr

    def strFace(self, sideNum):
        faceStr = self.faceDict[sideNum] + "\n"
        for j in range(3):
            for k in range(3):
                faceStr += self.cube[sideNum][3*j + k].name + " "
            faceStr += "\n"
        return faceStr

    def getAdjacentFaces(self, faceNum: int) -> List[List[Color]]:

        if (faceNum == 0):

            bottom = self.cube[3]
            top = self.cube[1]
            left = self.cube[4]
            right = self.cube[2]

        elif (faceNum == 5):

            bottom = self.cube[1]
            top = self.cube[3]
            left = self.cube[4]
            right = self.cube[2]


        else:
            bottom = self.cube[0]
            top = self.cube[5]

            # edge case if face is 1
            if (faceNum == 1):
                left = self.cube[4]
            else:
                left = self.cube[(faceNum + 3) % 4]

            # edge case if face is 4
            right = self.cube[faceNum % 4 + 1]

        return [bottom, right, top, left]

    def adjacentFacesTurn(self, faces: List[List[Color]], colors: List[int]):

        temps = copy.copy(faces[0])
        for i in range(3):
            faces[0][colors[i]] = faces[1][colors[i + 3]]
            faces[1][colors[i + 3]] = faces[2][colors[i + 6]]
            faces[2][colors[i + 6]] = faces[3][colors[i + 9]]
            faces[3][colors[i + 9]] = temps[colors[i]]

    def turn(self, faceNum: int, edgeList: List[int]) -> None:

        self.faceTurn(faceNum)

        faces = self.getAdjacentFaces(faceNum)

        temp = copy.copy(faces[0])


        self.adjacentFacesTurn(faces, edgeList)



    # Clockwise Face Turn
    def faceTurn(self, faceNum):
        # Current Face
        face = self.cube[faceNum]

        # Corners
        temp = face[0]
        face[0] = face[6]
        face[6] = face[8]
        face[8] = face[2]
        face[2] = temp

        # Edges
        temp2 = face[1]
        face[1] = face[3]
        face[3] = face[7]
        face[7] = face[5]
        face[5] = temp2

        # Other Faces

    def frontTurn(self):

        #             Bottom   Right    Top      Left
        self.turn(1, [0, 1, 2, 6, 3, 0, 8, 7, 6, 2, 5, 8])

    def rightTurn(self):

        #             Bottom   Right    Top      Left
        self.turn(2, [2, 5, 8, 6, 3, 0, 2, 5, 8, 2, 5, 8])

    def backTurn(self):

        #             Bottom   Right    Top      Left
        self.turn(3, [8, 7, 6, 6, 3, 0, 0, 1, 2, 2, 5, 8])

    def leftTurn(self):

        #             Bottom   Right    Top      Left
        self.turn(4, [6, 3, 0, 6, 3, 0, 6, 3, 0, 2, 5, 8])

    def downTurn(self):

        #             Bottom   Right    Top      Left
        self.turn(0, [8, 7, 6, 8, 7, 6, 8, 7, 6, 8, 7, 6])

    def upTurn(self):

        #             Bottom   Right    Top      Left
        self.turn(5, [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2])

    def executeAlgorithm(self, alg: str):

        self.solveAlg += alg

        turns = {
            'F': self.frontTurn,
            'f': lambda: [self.frontTurn() for _ in range(3)],
            'R': self.rightTurn,
            'r': lambda: [self.rightTurn() for _ in range(3)],
            'B': self.backTurn,
            'b': lambda: [self.backTurn() for _ in range(3)],
            'L': self.leftTurn,
            'l': lambda: [self.leftTurn() for _ in range(3)],
            'D': self.downTurn,
            'd': lambda: [self.downTurn() for _ in range(3)],
            'U': self.upTurn,
            'u': lambda: [self.upTurn() for _ in range(3)],
        }

        for char in alg:
            if char in turns:
                turns[char]()

    def edgeFinder(self, color1: Color, color2: Color) -> int:
        edgeList = [
            ((1, 7), (0, 1), 0),
            ((2, 7), (0, 5), 1),
            ((3, 7), (0, 7), 2),
            ((4, 7), (0, 3), 3),
            ((1, 5), (2, 3), 4),
            ((2, 5), (3, 3), 5),
            ((3, 5), (4, 3), 6),
            ((4, 5), (1, 3), 7),
            ((1, 1), (5, 7), 8),
            ((2, 1), (5, 5), 9),
            ((3, 1), (5, 1), 10),
            ((4, 1), (5, 3), 11),

        ]
        for edge in edgeList:
            coords1, coords2, pos = edge
            face1, pos1 = coords1
            face2, pos2 = coords2
            if color1 == self.cube[face1][pos1]:
                if color2 == self.cube[face2][pos2]:
                    return pos
            if color2 == self.cube[face1][pos1]:
                if color1 == self.cube[face2][pos2]:
                    return pos + 12

    def pieceShifter(self, currEdge: int) -> int:
        if currEdge % 4 == 0:
            return currEdge + 3
        return currEdge - 1

    def crossAlg(self, edgePos: int) -> str:

        crossAlgs: List[str] = [
            "FdLD",
            "RF",
            "BDRd",
            "lf",
            "Drd",
            "DDbDD",
            "dlD",
            "f",
            "ULfl",
            "rFR",
            "urFR",
            "Lfl",
            "",
            "RRUFF",
            "BBUUFF",
            "LLuFF",
            "F",
            "DRd",
            "DDBDD",
            "dLD",
            "FF",
            "UFF",
            "UUFF",
            "uFF"
        ]

        return crossAlgs[edgePos]

    def algShifter(self, currAlg: str) -> str:

        shifts: Dict[str, str] = {
            "F": "R",
            "f": "r",
            "R": "B",
            "r": "b",
            "B": "L",
            "b": "l",
            "L": "F",
            "l": "f",
        }

        newAlg: str = ""
        for char in currAlg:
            if char in shifts:
                newAlg += shifts[char]
            else:
                newAlg += char
        return newAlg

    def oneCrossEdge(self, color: Color, numShifts: int) -> None:
        edgePos = self.edgeFinder(Color.W, color)

        for _ in range(numShifts):
            edgePos = self.pieceShifter(edgePos)

        edgeAlg = self.crossAlg(edgePos)

        for _ in range(numShifts):
            edgeAlg = self.algShifter(edgeAlg)

        self.executeAlgorithm(edgeAlg)

    def cross(self):
        self.oneCrossEdge(Color.R, 0)
        self.oneCrossEdge(Color.G, 1)
        self.oneCrossEdge(Color.O, 2)
        self.oneCrossEdge(Color.B, 3)
        print("Cross Complete")


    def cornerFinder(self, color1: Color, color2: Color, color3: Color) -> int:

        cornerList = [
            ((1, 8), (2, 6), (0, 2), 0),
            ((2, 8), (3, 6), (0, 8), 1),
            ((3, 8), (4, 6), (0, 6), 2),
            ((4, 8), (1, 6), (0, 0), 3),
            ((1, 2), (5, 8), (2, 0), 4),
            ((2, 2), (5, 2), (3, 0), 5),
            ((3, 2), (5, 0), (4, 0), 6),
            ((4, 2), (5, 6), (1, 0), 7),
        ]

        for corner in cornerList:
            coords1, coords2, coords3, pos = corner
            face1, pos1 = coords1
            face2, pos2 = coords2
            face3, pos3 = coords3
            if color1 == self.cube[face1][pos1]:
                if color2 == self.cube[face2][pos2]:
                    if color3 == self.cube[face3][pos3]:
                        return pos
            if color2 == self.cube[face1][pos1]:
                if color3 == self.cube[face2][pos2]:
                    if color1 == self.cube[face3][pos3]:
                        return pos + 8
            if color3 == self.cube[face1][pos1]:
                if color1 == self.cube[face2][pos2]:
                    if color2 == self.cube[face3][pos3]:
                        return pos + 16

    def pairFinder(self, color1: Color, color2: Color, color3: Color, numShifts: int) -> Tuple[int, int]:

        corner = self.cornerFinder(color1, color2, color3)
        edge = self.edgeFinder(color2, color3)
        for _ in range(numShifts):
            corner = self.pieceShifter(corner)
            edge = self.pieceShifter(edge)

        return corner, edge

    # If corner % 8 is 1, 2, or 3, do specific move for each
    # If edge % 12 is 5, 6, 7, do specific move
    def hiddenF2LPieces(self, pairPos: Tuple[int, int], color2: Color, color3: Color, numShifts: int):

        cornerPos = pairPos[0] % 8
        cornerAlgs: Dict[int, str] = {
            1: "rUURu",
            2: "LUUl",
            3: "luL"
        }
        if cornerPos in cornerAlgs:
            cornerAlg = cornerAlgs[cornerPos]
            for _ in range(numShifts):
                cornerAlg = self.algShifter(cornerAlg)
            self.executeAlgorithm(cornerAlg)

        edgePos = self.edgeFinder(color2, color3)
        for _ in range(numShifts):
            edgePos = self.pieceShifter(edgePos)

        edgePos = edgePos % 12
        edgeAlgs: Dict[int, str] = {
            5: "rUR",
            6: "Lul",
            7: "luL"
        }

        if edgePos in edgeAlgs:
            edgeAlg = edgeAlgs[edgePos]
            for _ in range(numShifts):
                edgeAlg = self.algShifter(edgeAlg)
            self.executeAlgorithm(edgeAlg)


    def F2LNormalCase(self, color1: Color, color2: Color, color3: Color, numShifts: int) -> str:

        pairPos = self.pairFinder(color1, color2, color3, numShifts)
        self.hiddenF2LPieces(pairPos, color2, color3, numShifts)
        pairPos = self.pairFinder(color1, color2, color3, numShifts)

        F2LAlgs: Dict[Tuple[int, int], str] = {
            (4, 21): "URur",
            (4, 11): "fuF",
            (12, 8): "ufUF",
            (12, 22): "RUr",
            (4, 10): "uRurUfuF",
            (4, 9): "uRUUrUfuF",
            (4, 8): "UfUFufuF",
            (12, 23): "uRUrURUr",
            (12, 20): "rUURRURRUR",
            (12, 21): "uRurURUr",
            (4, 22): "uRUrUURur",
            (4, 23): "uRUUrUURur",
            (12, 11): "UfuFUUfUF",
            (12, 10): "UfUUFUUfUF",
            (20, 22): "URUUrURur",
            (20, 23): "UURUrURur",
            (20, 11): "ufUUFufUF",
            (20, 10): "UUfuFufUF",
            (4, 20): "fUFUURUr",
            (20, 21): "RUUruRUr",
            (20, 20): "URuruRurURur",
            (12, 9): "RurUUfuF",
            (20, 8): "fUUFUfuF",
            (20, 9): "FURurfRur",
            (8, 21): "rfRURurF",
            (0, 21): "RurURur",
            (0, 8): "rFRfURur",
            (8, 8): "URurufUF",
            (16, 8): "fUFufUF",
            (16, 21): "RUruRUr",
            (20, 16): "urFRfRur",
            (4, 4): "uRurUURur",
            (4, 16): "uRUrUfuF",
            (20, 4): "URurURurURur",
            (12, 4): "URUrUURUr",
            (12, 16): "UfuFuRUr",
            (8, 4): "",
            (0, 4): "RuruRUrUURur",
            (0, 16): "fUFUURUrURur",
            (8, 16): "RurUfUUFUUfUR",
            (16, 4): "RurURUUrURur",
            (16, 16): "RUruRurUUfuF",
        }
        for _ in range(4):
            if pairPos in F2LAlgs:
                return F2LAlgs[pairPos]
            self.upTurn()
            self.solveAlg += "U"
            pairPos = self.pairFinder(color1, color2, color3, numShifts)

    def F2LPair(self, color1: Color, color2: Color, color3: Color, numShifts: int):

        # move the corner and edge to top layer if not there

        alg: str = self.F2LNormalCase(color1, color2, color3, numShifts)
        for _ in range(numShifts):
            alg = self.algShifter(alg)

        self.executeAlgorithm(alg)

    def F2L(self):

        self.F2LPair(Color.W, Color.R, Color.G, 0)
        self.F2LPair(Color.W, Color.G, Color.O, 1)
        self.F2LPair(Color.W, Color.O, Color.B, 2)
        self.F2LPair(Color.W, Color.B, Color.R, 3)
        print("F2L Complete")

    def ollTopAnalysis(self) -> str:
        yellowBool: str = ""
        for i in range(9):
            if (self.cube[5][i] == Color.Y):
                yellowBool += "1"
            else:
                yellowBool += "0"
        return yellowBool

    def ollTopIdentifier(self) -> str:
        ollTopDict: Dict[str, str] = {
            "101110010": "RandomTop",
            "010110101": "RandomBottom",
            "001111100": "RightZ",
            "100111001": "LeftZ",
            "000111101": "C",
            "111110101": "BigArrow",
            "101111101": "H",
            "010111010": "Cross",
            "010111111": "Tank",
            "011111110": "8",
            "010111110": "Sune",
            "000010000": "Dot",
            "100010000": "CornerDot",
            "100010001": "Diagonal",
            "101010000": "Whiskers",
            "101010101": "Checker",
            "001110010": "SmallArrow",
            "100011011": "DualSquare",
            "000111000": "Line",
            "000111100": "RightGun",
            "000111001": "LeftGun",
            "110110100": "p",
            "011011001": "q",
            "010110000": "SmallL",
            "110011000": "LeftTetris",
            "011110000": "RightTetris",
            "110110000": "Square",
            "001111001": "T",
            "110011001": "W",
            "111111111": "Solved"
        }

        for _ in range(4):
            yellowBool: str = self.ollTopAnalysis()
            if yellowBool in ollTopDict:
                return ollTopDict[yellowBool]
            # Don't forget to add these turns to the output string
            self.upTurn()
            self.solveAlg += "U"





    def ollAdjAnalysis(self) -> str:
        adjBool: str = ""
        for i in range(4):
            for j in range(3):
                if (self.cube[i + 1][j] == Color.Y):
                    adjBool += "1"
                else:
                    adjBool += "0"
        return adjBool

    def ollAdjIdentifier(self, shape: str) -> str:

        ollAlgs: Dict[str, Dict[str, str]] = {
            "RandomTop": {
                "000110010001": "URUruRurfuFRUr",
                "101010010000": "ruRurUURFRUruf"
            },
            "RandomBottom": {
                "010011000100": "FrFRRuruRRrFF",
                "010010101000": "RUrURUUrFRUruf"
            },
            "RightZ": {
                "010100011000": "LfluLUFul"
            },
            "LeftZ": {
                "010000110001": "rFRUrufUR"
            },
            "C": {
                "010001010100": "RURRurFRURuf",
                "010000111000": "UrurFRfUR"
            },
            "BigArrow": {
                "010010000000": "LFrflRURur"
            },
            "H": {
                "010000010000": "RUruLrFRfl"
            },
            "Cross": {
                "101000101000": "RUUruRUruRur",
                "001000100101": "RUURRuRRuRRUUR"
            },
            "Tank": {
                "000000101000": "RRdRUUrDRUUR",
                "000001000100": "uLFrflFRf"
            },
            "8": {
                "001000000100": "fLFrflFR"
            },
            "Sune": {
                "000100100100": "UURUUruRur",
                "001001001000": "RUrURUUr"
            },
            "Dot": {
                "010111010111": "RUURRFRfUUrfRf",
                "010001000011": "LFlUULFFrFFRfl"
            },
            "CornerDot": {
                "011011010011": "ulRRBrBLUUlBLr",
                "110110110010": "UUlRbLUUlbRbrLr"
            },
            "Diagonal": {
                "110011010010": "FrfRRlBRbrbLr"
            },
            "Whiskers": {
                "111010010010": "LFrFRFFLLbRbrBBL",
                "010110010011": "lRBRBrbLrrFRf"
            },
            "Checker": {
                "010010010010": "LFrfLLRRBRbrbLr"
            },
            "SmallArrow": {
                "100110010100": "URUrurFRRUruf",
                "001010011001": "RUrUrFRfRUUr"
            },
            "DualSquare": {
                "100001010010": "RUURRFRfRUUr",
                "000000110011": "UUFrfRURur"
            },
            "Line": {
                "110101011000": "FURurURurf",
                "010100111001": "URUrURuBubr",
                "111000111000": "rFRURuRRfRRurURUr",
                "010101010101": "lbLurURurURlBL"
            },
            "RightGun": {
                "011001011000" : "FURuRRfRURur",
                "010100110100": "UULFlRUruLfl"
            },
            "LeftGun": {
                "110000110100": "rFRUrfRFuf",
                "010001011001": "UUrfRluLUrFR"
            },
            "p": {
                "011010100000": "LUfulULFl",
                "010111000000": "FURurf"
            },
            "q": {
                "110000001010": "ruFURurfR",
                "010000000111": "fulULF"
            },
            "SmallL": {
                "010110101001": "UrurFRfrFRfUR",
                "011010100101": "FRUruRUruf",
                "111011000100": "ULfLLBLLFLLbL",
                "110111001000": "UUlBLLfLLbLLFl",
                "010111000101": "UrFFLFlfLFlFR",
                "111010101000": "LFFrfRFrfRfl",

            },
            "LeftTetris": {
                "011001000011": "uLFrFRFFl",
                "110100100010": "LRRfRfrFFRfRl"
            },
            "RightTetris": {
                "110110000100": "UrfLflFFR",
                "011010001001": "LFrFrDRdRFFl"
            },
            "Square": {
                "011011000001": "rFFLFlFR",
                "110110100000": "ULFFrfRfl"
            },
            "T": {
                "110000011000": "RUrurFRf",
                "010000010101": "FRUruf"
            },
            "W": {
                "010000100011": "luLulULULflF",
                "110001000010": "RUrURururFrf"
            },
            "Solved": {
                "000000000000": ""
            }
        }



        for _ in range(4):
            adjBool: str = self.ollAdjAnalysis()
            if adjBool in ollAlgs[shape]:
                return ollAlgs[shape][adjBool]
            # Don't forget to add these turns to the output string
            self.upTurn()
            self.solveAlg += "U"

    def oll(self):

        shape: str = self.ollTopIdentifier()
        alg: str = self.ollAdjIdentifier(shape)
        self.executeAlgorithm(alg)
        if (self.ollTopIdentifier() == "Solved"):
            print("OLL Complete")

    def pllAdjAnalysis(self) -> str:

        adjStr: str = ""

        for i in range(4):
            for j in range(3):
                adjStr += str(self.cube[i + 1][j].name)

        return adjStr

    def pllShifter(self, adjStr: str) -> str:
        shiftedStr: str = ""
        for char in adjStr:
            if char == "R":
                shiftedStr += "B"
            elif char == "B":
                shiftedStr += "O"
            elif char == "O":
                shiftedStr += "G"
            else:
                shiftedStr += "R"

        return shiftedStr

    def pllIdentifier(self) -> str:
        # Create a dictionary of each pll case and its alg
        pllAlgs: Dict[str, str] = {
            "OBBRROBGRGOG": "LLBBlfLBBlFl",
            "RBGORRGGOBOB": "LLFFLBlFFLbL",
            "BGRGRBRBGOOO": "rufRUrurFRRuruRUrUR",
            "BRRGOBRBGOGO": "RRUrUruRuRRuDrURd",
            "BGRGBBROGORO": "ruRUdRRurURuRuRRD",
            "BGRGOBRRGOBO": "RRuRuRUrURRUdRurD",
            "BORGGBRBGORO": "RUruDRRuRurUrURRd",
            "BBRGGBRRGOOO": "RRDRdRFFlULFF",
            "OBBROOBRRGGG": "RUrfRUrurFRRur",
            "OOBRBOBGRGRG": "RuruRURDruRdrUUr",
            "RBGOGRGOOBRB": "RRFRURurfRUUrUUR",
            "BBRGOBRGOBOG": "RUrurFRRuruRUrf",
            "OBRGRBRGOBOG": "lBLflbLFlbLflBLF",
            "GBBROOBGGORR": "RUrURUrfRUrurFRRurUURur",
            "BBGOORGGBRRO": "rURurfuFRUrFrfRuR",
            "BBGOGRGRBROO": "rUruRdrDrUdRRuRRdRR",
            "BBGORRGOBRGO": "FRuruRUrfRUrurFRf",
            "BGBRORGBGORO": "LLRRDLLRRUULLRRDLLRR",
            "BRBRORGGGOBO": "LLRRDlRFFLrDLLRR",
            "BOBRBRGGGORO": "LLRRdlRFFLrdLLRR",
            "OGOBRBRBRGOG": "LrFLLRRBLLRRFLrDDLLRR",
            "RRRGGGOOOBBB": ""
        }

        for _ in range(4):
            case: str = self.pllAdjAnalysis()
            for i in range(4):
                if case in pllAlgs:
                    return pllAlgs[case]
                case = self.pllShifter(case)
            # Don't forget to add these turns to the output string
            self.upTurn()
            self.solveAlg += "U"




    def pll(self):
        alg: str = self.pllIdentifier()
        self.executeAlgorithm(alg)
        if (self.pllIdentifier() == ""):
            print("PLL Complete")

    def finalMove(self):
        for _ in range(4):
            if self.cube[1][0] == Color.R:
                print("Solved")
                return
            self.upTurn()
            self.solveAlg += "U"

    def moveCounter(self):
        i = 0
        ctr = 0
        print("Number of Moves:")
        while i < len(self.solveAlg):

            ctr += 1

            if (i + 1) >= len(self.solveAlg):
                print(ctr)
                return

            if self.solveAlg[i] == self.solveAlg[i + 1]:
                i += 1
            i += 1


    def solve(self):
        self.cross()
        self.F2L()
        self.oll()
        self.pll()
        self.finalMove()
        self.solveAlg = algCompresser(self.solveAlg)
        self.moveCounter()
        print("Solution:", self.solveAlg)

    def fullSolve(self, scramble: str) -> None:
        self.executeAlgorithm(scramble)
        print(self)
        self.solveAlg = ""
        self.scramble = scramble
        self.solve()


def removeTriples(alg: str) -> str:

        # Replace Triple Moves: RRR -> r or ddd -> D
        newStr: str = ""
        i = 0

        while i < len(alg):

            if i + 2 < len(alg) and alg[i] == alg[i + 1] == alg[i + 2]:
                newStr += alg[i].swapcase()
                i += 3
            else:
                newStr += alg[i]
                i += 1

        return newStr

def removeReversals(alg: str) -> str:

    newStr: str = ""
    i = 0

    while i < len(alg):

        currChar: str = alg[i]
        flippedChar: str = currChar.swapcase()

        if i + 1 < len(alg) and flippedChar == alg[i + 1]:
            i += 2
        else:
            newStr += alg[i]
            i += 1

    return newStr

def algCompresser(alg: str) -> str:

    newStr: str = ""

    while alg != newStr:

        newStr = alg
        alg = removeTriples(alg)
        alg = removeReversals(alg)

    return alg




if __name__ == '__main__':
    c = Cube()
    c.fullSolve("RRurUlFFufLDFFLLBBUULLUURRBD")