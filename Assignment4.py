##
# CPSC 217 Assignment 4
# Name: Anil Mawji
# UCID: 30099809
#
# Program Description: Draws a Sankey diagram to the screen using data from an external text file

import sys
import math
from SimpleGraphics import *

WIDTH = getWidth()
HEIGHT = getHeight()
PADDING_X = 150
PADDING_Y = 75
SPACING_X = 10
SPACING_Y = 10
BAR_WIDTH = 25
COLORS = [
    (230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200), (245, 130, 48), (145, 30, 180), (70, 240, 240),
    (240, 50, 230), (210, 245, 60), (250, 190, 190), (0, 128, 128), (230, 190, 255), (170, 110, 40), (255, 250, 200),
    (128, 0, 0), (170, 255, 195), (128, 128, 0), (255, 215, 180), (0, 0, 128), (128, 128, 128), (255, 255, 255)
]
DEFAULT_SOURCE_COLOR = COLORS[1]


# Draws a new Sankey diagram the screen
#
# @param data  a dictionary containing destination names as keys and amounts of flow as values
# @return None
def draw_sankey(data):
    # Calculate the bar info
    total_flow = sum(value[0] for value in list(data.values())[2:])  # Trim title and source from data
    num_pixels = HEIGHT - PADDING_Y * 2 - (len(data) - 1) * SPACING_Y
    pixels_per_unit = num_pixels / total_flow

    # Draw the source bar
    source_x = PADDING_X + SPACING_X
    source_y = (HEIGHT - total_flow * pixels_per_unit) / 2
    source_height = total_flow * pixels_per_unit
    source_color = data["Source"][1]
    setColor(*source_color)
    rect(source_x, source_y, BAR_WIDTH, source_height)

    # Draw a border around the source bar
    setColor("black")
    line(source_x, source_y, source_x + BAR_WIDTH, source_y)
    line(source_x, source_y, source_x, source_y + source_height)
    line(source_x, source_y + source_height, source_x + BAR_WIDTH, source_y + source_height)

    # Draw the title
    setFont("Calibri", "20")
    text(WIDTH / 2, 35, data["Title"])
    # Draw the source bar text
    setFont("Calibri")
    text(PADDING_X, HEIGHT / 2, data["Source"][0], "e")

    # Calculate the position of the destination bar
    dest_x = WIDTH - PADDING_X
    dest_y = PADDING_Y

    for k in dict(list(data.items())[2:]):  # Trim title and source from data
        # Retrieve the color of the destination bar
        dest_color = data[k][1]
        # Calculate the height of the destination bar
        dest_height = data[k][0] * pixels_per_unit
        # Draw the destination bar
        setColor(*dest_color)
        rect(dest_x, dest_y, BAR_WIDTH, dest_height)

        # Draw the body of the diagram
        range_x = dest_x - source_x - BAR_WIDTH
        for x in range(range_x):
            # Calculate the vertical offset of the current line being drawn
            offset_y = (math.sin(x / range_x * math.pi - math.pi / 2) + 1) / 2 * (source_y - dest_y)
            # Calculate the color of the current line being drawn
            setColor(source_color[0] + (x / range_x) * (dest_color[0] - source_color[0]),
                     source_color[1] + (x / range_x) * (dest_color[1] - source_color[1]),
                     source_color[2] + (x / range_x) * (dest_color[2] - source_color[2]))
            # Draw the current line
            line(source_x + BAR_WIDTH + x, source_y - offset_y,
                 source_x + BAR_WIDTH + x, source_y + dest_height - offset_y)
            # Draw a border pixel above the current line
            setColor("black")
            line(source_x + BAR_WIDTH + x, source_y - offset_y,
                 source_x + BAR_WIDTH + x + 1, source_y - offset_y)
            # Draw a border pixel below the current line
            line(source_x + BAR_WIDTH + x, source_y - offset_y + dest_height,
                 source_x + BAR_WIDTH + x + 1, source_y - offset_y + dest_height)

        # Draw the destination text
        setColor("black")
        text(dest_x + BAR_WIDTH + SPACING_X, dest_y + dest_height / 2, k, "w")

        # Draw a border around destination bar
        line(dest_x, dest_y, dest_x + BAR_WIDTH, dest_y)
        line(dest_x + BAR_WIDTH, dest_y, dest_x + BAR_WIDTH, dest_y + dest_height)
        line(dest_x, dest_y + dest_height, dest_x + BAR_WIDTH, dest_y + dest_height)

        # Increment the y values to prepare for drawing the next bar
        source_y += dest_height
        dest_y += dest_height + SPACING_Y


# Gathers data for drawing a Sankey diagram from a text file.
# Data is read into the program sequentially.
#
# @param file  the file containing the data
# @return data a dictionary containing destination names as keys and amounts of flow as values
def collect_data(file):
    # Insert the title as the first key in the dictionary
    data = {"Title": file.readline().rstrip()}
    for i, ln in enumerate(file):
        ln = ln.split(",")
        if i == 0:
            # Source data is a list that holds the source title and a color
            # If 3 more numbers for the color are not found in the line, use the default source color
            data["Source"] = [ln[0].rstrip(), DEFAULT_SOURCE_COLOR]\
                if len(ln) < 4 else [ln[0].rstrip(), list(map(float, ln[1:4]))]
        else:
            # Destination data is a list that holds the flow value and a color
            # If 3 more numbers for the color are not found in the line, use the default destination color
            data[ln[0]] = [float(ln[1]), COLORS[i + list(COLORS).index(DEFAULT_SOURCE_COLOR)]]\
                if len(ln) < 5 else [float(ln[1]), list(map(float, ln[2:5]))]
    return data


def main():
    setWindowTitle("Assignment 4")
    background("light gray")
    # Get file name from command line arguments if one exists, otherwise ask the user for the file name directly
    file_name = sys.argv[1] if len(sys.argv) == 2\
        else input("Enter the name of the file: ") if len(sys.argv) == 1 else None
    if file_name:
        try:
            file = open(file_name)
            data = collect_data(file)
            print(data)
            draw_sankey(data)
            file.close()
        except FileNotFoundError:
            print("Error: A file with that name does not exist.")
        except IOError:
            print("Error: An error occurred while opening the file.")
    else:
        print("Error: Too many command line arguments were provided.\nUsage:", sys.argv[0], "<file name>")


if __name__ == '__main__':
    main()
