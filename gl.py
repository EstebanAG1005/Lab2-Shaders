# Lab2-Shaders
# Graficas por computadora 
# Esteban Aldana Guerra 20591

import struct
from textures import Obj
from collections import namedtuple
from math import sqrt

V2 = namedtuple('Vertex2', ['x', 'y'])
V3 = namedtuple('Vertex3', ['x', 'y', 'z'])

# -------------------------------------------- Utils ---------------------------------------------------

# 1 byte
def char(c):
    return struct.pack('=c', c.encode('ascii'))

# 2 bytes
def word(c):
    return struct.pack('=h', c)

# 4 bytes 
def dword(c):
    return struct.pack('=l', c)

# Funciones de Colores
def normalizeColorArray(colors_array):
    return [round(i * 255) for i in colors_array]

def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

# ----------------------------- Parte de Operaciones Matematicas -----------------------------------------

# funcion de Suma
def sum(v0, v1):
    return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

# funcion de resta    
def sub(v0, v1):
    return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

# multiplicacion    
def mul(v0, k):
    return V3(v0.x * k, v0.y * k, v0.z * k)

# producto punto
def dot(v0, v1):
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

# Regresa el largo del vector
def length(v0):
    return (v0.x ** 2 + v0.y ** 2 + v0.z ** 2) ** 0.5

# Normal del vector   
def norm(v0):
    v0length = length(v0)
    if not v0length:
        return V3(0, 0, 0)
    return V3(v0.x / v0length, v0.y / v0length, v0.z / v0length)

# 2 vectores de tamaño 2 que definen el rectángulo delimitador más pequeño posible  
def bbox(*vertices):
    xs = [vertex.x for vertex in vertices]
    ys = [vertex.y for vertex in vertices]
    xs.sort()
    ys.sort()
    xmin = xs[0]
    xmax = xs[-1]
    ymin = ys[0]
    ymax = ys[-1]
    return xmin, xmax, ymin, ymax

# Obtiene 2 valores de 3 vectores y devuelve un vector 3 con el producto punto
def cross(v1, v2):
    return V3(
        v1.y * v2.z - v1.z * v2.y, v1.z * v2.x - v1.x * v2.z, v1.x * v2.y - v1.y * v2.x,)

# Coordenadas Baricentricas
def barycentric(A, B, C, P):
    cx, cy, cz = cross(
        V3(B.x - A.x, C.x - A.x, A.x - P.x), V3(B.y - A.y, C.y - A.y, A.y - P.y),)
    if abs(cz) < 1:
        return -1, -1, -1
    u = cx / cz
    v = cy / cz
    w = 1 - (cx + cy) / cz
    return w, v, u

class Render(object):
    def __init__(self):
        self.framebuffer = []
        self.width = 600
        self.height = 600
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_width = 1000
        self.viewport_height = 1000
        self.glClear()
        self.zbuffer = [
            [-float('inf') for x in range(self.width)] for y in range(self.height)
        ]
        self.shape = None

    def glClear(self):
        r, g, b = 0, 0, 0
        bg_color = color(r, g, b)
        self.framebuffer = [
            [bg_color for x in range(self.width)] for y in range(self.height)
        ]

    def glCreateWindow(self, width, height):
        self.height = height
        self.width = width

    def glClearColor(self, r=1, g=1, b=1):
        normalized = normalizeColorArray([r, g, b])
        clearColor = color(normalized[0], normalized[1], normalized[2])

        self.framebuffer = [
            [clearColor for x in range(self.width)] for y in range(self.height)
        ]

    def glViewport(self, x, y, width, height):
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_height = height
        self.viewport_width = width

    def point(self, x, y, color):
        self.framebuffer[y][x] = color

    def triangle(self, A, B, C):
        xmin, xmax, ymin, ymax = bbox(A, B, C)

        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                P = V2(x, y)
                w, v, u = barycentric(A, B, C, P)
                if w < 0 or v < 0 or u < 0:
                    # point is outside
                    continue

                z = A.z * u + B.z * v + C.z * w

                r, g, b = self.shaders(
                    x, y
                )

                shader_color = color(r, g, b)

                if z > self.zbuffer[y][x]:
                    self.point(x, y, shader_color)
                    self.zbuffer[y][x] = z

    def radio(self,x,y):
        return int(sqrt(x*x + y*y))

    def shaders(self, x=0, y=0):

        shader_color = 0, 0, 0
        current_shape = self.shape

        r1, g1, b1 = 0, 0, 0
        r2, g2, b2 = 0, 0, 0
        percentage = 1

        if current_shape == jupiter:
            if y >= 375 and y <= 425:
                r1, g1, b1 = 115, 145, 170
                r2, g2, b2 = 136, 195, 222
                percentage = abs(y - 400)

            if (y > 325 and y < 375) or (y > 425 and y < 475):
                if y < 450 or y > 350:
                    r1, g1, b1 = 136, 195, 222
                    r2, g2, b2 = 156, 152, 164
                    percentage = abs(y - 400)

                    if y >= 450 or y <= 350:
                        r1, g1, b1 = 115, 145, 170
                        r2, g2, b2 = 156, 152, 164
                        if y < 450 or y > 350:
                            r1, g1, b1 = 156, 152, 164
                            r2, g2, b2 = 156, 152, 164
                            percentage = abs(y - 400)

                            if y >= 450 or y <= 350:
                                r1, g1, b1 = 156, 152, 164
                                r2, g2, b2 = 156, 152, 164

                if y >= 450 or y <= 350:
                    r1, g1, b1 = 115, 145, 170
                    r2, g2, b2 = 156, 152, 164
                    if y >= 450:
                        percentage = abs(y - 450)
                    else:
                        percentage = abs(y - 350)

            if (y <= 325 and y >= 260) or (y <= 540 and y >= 475):
                if y < 500 or y > 300:
                    r1, g1, b1 = 156, 152, 164
                    r2, g2, b2 = 136, 195, 222                    
                    if y <= 325:
                        percentage = abs(y - 350)
                    else:
                        percentage = abs(y - 450)

                if y >= 500 or y <= 300:
                    r1, g1, b1 = 136, 195, 222
                    r2, g2, b2 = 115, 145, 170
                    if y <= 300:
                        percentage = abs(y - 300)
                    else:
                        percentage = abs(y - 500)
                
            # Gradientes
            percentage = (percentage / 50)
            r = r1 + percentage * (r2 - r1)
            g = g1 + percentage * (g2 - g1)
            b = b1 + percentage * (b2 - b1)
            shader_color = r, g, b

            if (y % 40) in range(0, 14):
                r, g, b = shader_color
                r *= 0.98
                g *= 0.98
                b *= 0.98
                shader_color = r, g, b

        b, g, r = shader_color
        b /= 255
        g /= 255
        r /= 255

        intensity = 1

        if current_shape == jupiter:
            intensity = (self.radio(x - 120, y - 390) + 50) / 400
            intensity = 1 - (intensity * 0.95) ** 4

        b *= intensity
        g *= intensity
        r *= intensity

        if intensity > 0:
            return r, g, b
        else:
            return 0, 0, 0

    def glLoad(self, filename="default.obj", tras=[0, 0], size=[1, 1], shape=None):
        model = Obj(filename)
        self.shape = shape

        for face in model.faces:
            vcount = len(face)

            if vcount == 3:
                face1 = face[0][0] - 1
                face2 = face[1][0] - 1
                face3 = face[2][0] - 1

                v1 = model.vertices[face1]
                v2 = model.vertices[face2]
                v3 = model.vertices[face3]

                x1 = round((v1[0] * size[0]) + tras[0])
                y1 = round((v1[1] * size[1]) + tras[1])
                z1 = round((v1[2] * size[2]) + tras[2])

                x2 = round((v2[0] * size[0]) + tras[0])
                y2 = round((v2[1] * size[1]) + tras[1])
                z2 = round((v2[2] * size[2]) + tras[2])

                x3 = round((v3[0] * size[0]) + tras[0])
                y3 = round((v3[1] * size[1]) + tras[1])
                z3 = round((v3[2] * size[2]) + tras[2])

                a = V3(x1, y1, z1)
                b = V3(x2, y2, z2)
                c = V3(x3, y3, z3)

                self.triangle(a, b, c)

            else:
                face1 = face[0][0] - 1
                face2 = face[1][0] - 1
                face3 = face[2][0] - 1
                face4 = face[3][0] - 1

                v1 = model.vertices[face1]
                v2 = model.vertices[face2]
                v3 = model.vertices[face3]
                v4 = model.vertices[face4]

                x1 = round((v1[0] * size[0]) + tras[0])
                y1 = round((v1[1] * size[1]) + tras[1])
                z1 = round((v1[2] * size[2]) + tras[2])

                x2 = round((v2[0] * size[0]) + tras[0])
                y2 = round((v2[1] * size[1]) + tras[1])
                z2 = round((v2[2] * size[2]) + tras[2])

                x3 = round((v3[0] * size[0]) + tras[0])
                y3 = round((v3[1] * size[1]) + tras[1])
                z3 = round((v3[2] * size[2]) + tras[2])

                x4 = round((v4[0] * size[0]) + tras[0])
                y4 = round((v4[1] * size[1]) + tras[1])
                z4 = round((v4[2] * size[2]) + tras[2])

                a = V3(x1, y1, z1)
                b = V3(x2, y2, z2)
                c = V3(x3, y3, z3)
                d = V3(x4, y4, z4)

                self.triangle(a, b, c)
                self.triangle(a, c, d)

    def finish(self, filename="out.bmp"):
        f = open(filename, "bw")

        f.write(char("B"))
        f.write(char("M"))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[x][y])
       
        f.close()

jupiter = "jupiter"

