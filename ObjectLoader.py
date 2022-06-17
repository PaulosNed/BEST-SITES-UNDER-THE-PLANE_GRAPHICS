import numpy as np


class ObjectLoader:
    def __init__(self) -> None:
        self.vertex_coordinates = []
        self.tex_coordinates = []
        self.normal_coordinates = []
        self.all_coordinates = []
        self.indices = []
        
    def getVertexArray(self, file):
        wholeObject = open(file, "r")
        for line in wholeObject.readlines():
            coordinates = line.split()
            if coordinates[0] == 'v':
                self.vertex_coordinates.append(coordinates[1:])
            elif coordinates[0] == 'vt':
                self.tex_coordinates.append(coordinates[1:])
            elif coordinates[0] == 'vn':
                self.normal_coordinates.append(coordinates[1:])
            elif coordinates[0] == 'f':
                for combination in coordinates[1:]:
                    eachCombo = combination.split("/")
                    full_coordinate = []

                    for item in self.vertex_coordinates[int(eachCombo[0])-1]:
                        full_coordinate.append(item)
                    
                    for item in self.tex_coordinates[int(eachCombo[1])-1]:
                        full_coordinate.append(item)

                    for item in self.normal_coordinates[int(eachCombo[2])-1]:
                        full_coordinate.append(item)           
                    
                    self.all_coordinates.append(full_coordinate)
                    self.indices.append(int(eachCombo[0])-1)
    
        return np.array(self.indices, dtype='uint32'), np.array(self.all_coordinates, dtype=np.float32)
                    