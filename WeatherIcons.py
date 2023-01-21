from inky import InkyWHAT

inky_display = InkyWHAT("yellow")
inky_display.set_border(inky_display.WHITE)

import math
import numbers

from PIL import Image, ImageFont, ImageDraw

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

def _compute_regular_polygon_vertices(bounding_circle, n_sides, rotation):
    # 1. Error Handling
    # 1.1 Check `n_sides` has an appropriate value
    if not isinstance(n_sides, int):
        raise TypeError("n_sides should be an int")
    if n_sides < 3:
        raise ValueError("n_sides should be an int > 2")

    # 1.2 Check `bounding_circle` has an appropriate value
    if not isinstance(bounding_circle, (list, tuple)):
        raise TypeError("bounding_circle should be a tuple")

    if len(bounding_circle) == 3:
        *centroid, polygon_radius = bounding_circle
    elif len(bounding_circle) == 2:
        centroid, polygon_radius = bounding_circle
    else:
        raise ValueError(
            "bounding_circle should contain 2D coordinates "
            "and a radius (e.g. (x, y, r) or ((x, y), r) )"
        )

    if not all(isinstance(i, (int, float)) for i in (*centroid, polygon_radius)):
        raise ValueError("bounding_circle should only contain numeric data")

    if not len(centroid) == 2:
        raise ValueError(
            "bounding_circle centre should contain 2D coordinates (e.g. (x, y))"
        )

    if polygon_radius <= 0:
        raise ValueError("bounding_circle radius should be > 0")

    # 1.3 Check `rotation` has an appropriate value
    if not isinstance(rotation, (int, float)):
        raise ValueError("rotation should be an int or float")

    # 2. Define Helper Functions
    def _apply_rotation(point, degrees, centroid):
        return (
            round(
                point[0] * math.cos(math.radians(360 - degrees))
                - point[1] * math.sin(math.radians(360 - degrees))
                + centroid[0],
                2,
            ),
            round(
                point[1] * math.cos(math.radians(360 - degrees))
                + point[0] * math.sin(math.radians(360 - degrees))
                + centroid[1],
                2,
            ),
        )

    def _compute_polygon_vertex(centroid, polygon_radius, angle):
        start_point = [polygon_radius, 0]
        return _apply_rotation(start_point, angle, centroid)

    def _get_angles(n_sides, rotation):
        angles = []
        degrees = 360 / n_sides
        # Start with the bottom left polygon vertex
        current_angle = (270 - 0.5 * degrees) + rotation
        for _ in range(0, n_sides):
            angles.append(current_angle)
            current_angle += degrees
            if current_angle > 360:
                current_angle -= 360
        return angles

    # 3. Variable Declarations
    angles = _get_angles(n_sides, rotation)

    # 4. Compute Vertices
    return [
        _compute_polygon_vertex(centroid, polygon_radius, angle) for angle in angles
    ]

bkgCol = inky_display.WHITE
prmCol = inky_display.BLACK
sndCol = inky_display.YELLOW

def myCircle(centerPos, radius, fillColour, outlineColour, outlineWidth):
    centerX = centerPos[0]
    centerY = centerPos[1]

    draw.ellipse([(centerX-radius,centerY-radius),(centerX+radius,centerY+radius)],
    fill=fillColour, outline=outlineColour, width=outlineWidth)

def myArc(centerPos, radius, start, end, fillColour, outlineWidth):
    centerX = centerPos[0]
    centerY = centerPos[1]

    draw.arc([(centerX-radius,centerY-radius),(centerX+radius,centerY+radius)], start,
    end, fill=fillColour, width=outlineWidth)

def star(bounding_circle, fillColour, lineLength, outlineWidth, n_lines, rotation):
    myOutVert = _compute_regular_polygon_vertices(bounding_circle, n_lines, rotation)
    myInVert = _compute_regular_polygon_vertices((bounding_circle[0],bounding_circle[1],
    bounding_circle[2] - lineLength), n_lines, rotation)

    for k in range(n_lines):
        #draw.line((myOutVert[k], myInVert[k]), fill=myBlack, width=width+6)
        draw.line((myOutVert[k], myInVert[k]), fill=fillColour, width=outlineWidth)
        #myCircle(myOutVert[k] , width/2.1, fill, None, 0)
        #myCircle(myInVert[k], width/2.1, fill, None, 0)

def myStars():
    draw.line([(200+24, 150-8), (236,142)], fill=prmCol, width=5)
    draw.line([(200+30, 150-14), (230,148)], fill=prmCol, width=5)

    myCircle((200+24, 150-8), 2, prmCol, None, 0)
    myCircle((200+36, 150-8), 2, prmCol, None, 0)

    myCircle((200+30, 150-14), 2, prmCol, None, 0)
    myCircle((200+30, 150-2), 2, prmCol, None, 0)

    draw.line([(200-2, 150-26), (222,124)], fill=prmCol, width=5)
    draw.line([(200+10, 150-38), (210,136)], fill=prmCol, width=5)

    myCircle((200-2, 150-26), 2, prmCol, None, 0)
    myCircle((200+22, 150-26), 2, prmCol, None, 0)

    myCircle((200+10, 150-38), 2, prmCol, None, 0)
    myCircle((200+10, 150-14), 2, prmCol, None, 0)
    
def myMoon():
    myCircle((200, 150), 48, sndCol, prmCol, 5)
    myCircle((200+18, 150-16), 40, bkgCol, None, 0)

    myArc((200+18, 150-16), 40, 47, 234, prmCol, 5)

def mySunny():
    myCircle((200, 150), 32, sndCol, prmCol, 5)
    star((200, 150, 64), prmCol, 22, 7, 8, 22.5)
    
def myCloudy():
    myCircle((200+20, 150), 42, bkgCol, None, 0)
    myCircle((200-32, 150+9), 33, bkgCol, None, 0)
    
    myArc((200+20, 150), 42, 203, 90, prmCol, 5)
    myArc((200-32, 150+9), 33, 90, 346, prmCol, 5)
    draw.line([(200+20, 150+41), (200-32, 150+41)], fill=prmCol, width=5)
    
    myCircle((200-2, 150+1), 2, prmCol, None, 0)
    
def myCloudWGap():
    myArc((200+20, 150), 42, 203, 90-23, prmCol, 5)
    myArc((200-32, 150+9), 33, 90+6, 346, prmCol, 5)
    
    myCircle((200-2, 150+1), 2, prmCol, None, 0)
    
    myCircle((200-35, 150+40), 2, prmCol, None, 0)

def mySmallSun():
    myCircle((200-20, 150-28), 21, sndCol, prmCol, 5)
    star((200-20, 150-28, 43), prmCol, 14, 7, 8, 22.5)
    
def mySmallCloud():
    myCircle((200+31, 150+29), 28, bkgCol, None, 0)
    myCircle((200-4, 150+35), 22, bkgCol, None, 0)
    draw.rectangle([(200-10, 150+25), (200+10, 150+70)], bkgCol, None, 0)

    myArc((200+31, 150+29), 28, 200, 90, prmCol, 5)
    myArc((200-4, 150+35), 22, 90, 346, prmCol, 5)
    draw.line([(200+31, 150+56), (200-4, 150+56)], fill=prmCol, width=5)
    
def mySmallMoon():
    myCircle((200-3, 150-34), 32, sndCol, prmCol, 5)
    myCircle((200+9, 150-45), 27, bkgCol, None, 0)

    myArc((200+9, 150-45), 27, 46, 230, prmCol, 5)

def myMostlySunny():
    mySunny()
    mySmallCloud()
    
def myMostlyCloudy():
    mySmallSun()
    myCloudy()

def myClearNight():
    myMoon()
    myStars()

def myMostlyClearNight():
    myMoon()
    mySmallCloud()
    
def myMostlyCloudyNight():
    mySmallMoon()
    myCloudy()
    
def myRaining():
    myCloudWGap()
    
    draw.line([(200-16, 150+30), (200-32, 150+58)], fill=prmCol, width=5)	#line1
    draw.line([(200-2, 150+30), (200-22, 150+65)], fill=prmCol, width=5)	#line2
    draw.line([(200+12, 150+30), (200-4, 150+58)], fill=prmCol, width=5)	#line3
    draw.line([(200+26, 150+30), (200-2, 150+79)], fill=prmCol, width=5)	#line4
    
    myCircle((200-16, 150+30), 2, prmCol, None, 0), myCircle((200-32, 150+58), 2, prmCol, None, 0)
    myCircle((200-2, 150+30), 2, prmCol, None, 0), myCircle((200-22, 150+65), 2, prmCol, None, 0)
    myCircle((200+12, 150+30), 2, prmCol, None, 0), myCircle((200-4, 150+58), 2, prmCol, None, 0)
    myCircle((200+26, 150+30), 2, prmCol, None, 0), myCircle((200-2, 150+79), 2, prmCol, None, 0)
    
def myDrizzle():
    myCloudWGap()
    # Rule is x-4 for y+7 to move down
    
    draw.line([(200-20, 150+37), (200-28, 150+51)], fill=prmCol, width=5)	#line1
    draw.line([(200+2, 150+23), (200-6, 150+37)], fill=prmCol, width=5)		#line2
    draw.line([(200-18, 150+58), (200-26, 150+72)], fill=prmCol, width=5)	#line2b
    draw.line([(200+4, 150+44), (200-4, 150+58)], fill=prmCol, width=5)		#line3
    draw.line([(200+26, 150+30), (200+18, 150+44)], fill=prmCol, width=5)	#line4
    draw.line([(200+6, 150+65), (200-2, 150+79)], fill=prmCol, width=5)		#line4b
    
    myCircle((200-20, 150+37), 2, prmCol, None, 0), myCircle((200-28, 150+51), 2, prmCol, None, 0)
    myCircle((200+2, 150+23), 2, prmCol, None, 0), myCircle((200-6, 150+37), 2, prmCol, None, 0)
    myCircle((200-18, 150+58), 2, prmCol, None, 0), myCircle((200-26, 150+72), 2, prmCol, None, 0)
    myCircle((200+4, 150+44), 2, prmCol, None, 0), myCircle((200-4, 150+58), 2, prmCol, None, 0)
    myCircle((200+26, 150+30), 2, prmCol, None, 0), myCircle((200+18, 150+44), 2, prmCol, None, 0)
    myCircle((200+6, 150+65), 2, prmCol, None, 0), myCircle((200-2, 150+79), 2, prmCol, None, 0)
    
    
#------------------------------------------------------------
    
myCircle((200, 150), 96, None, prmCol, 1)

myDrizzle()
#myRaining()

flipped = img.rotate(180)

inky_display.set_image(flipped)
inky_display.show()