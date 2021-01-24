"""
Python program to illustrate HoughLine 
method for line detection

Taken and cleaned from
    https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/
"""
# %%
import cv2
import numpy as np


# %%
# Reading the required image in
# which operations are to be done.
# Make sure that the image is in the same
# directory in which this python program is
# img = cv2.imread('data/lines.jpg')
# img = cv2.imread('data/spider-web.jpg')
img = cv2.imread('data/highway.jpg')


# %%
# get the edges
def get_edges(image):
    """Get the edges of an image.

    :param image: the image to get the edges of
    :returns:     the edges of the image"""
    # Convert the img to greyscale
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection method on the image
    result = cv2.Canny(grey, 50, 150, apertureSize=3)

    return result


edges = get_edges(img)


# %%
# get the lines
def get_lines(edge_image):
    """Get the lines from an edge image."""
    # This returns an array of r and theta values
    return cv2.HoughLines(edges, 1, np.pi / 180, 200)


lines = get_lines(edges)
if lines is None:
    lines = []
print(lines)


# %%
# draw all lines
def draw_line(target, dist_to_origin, theta):
    """Draw all lines on the image.

    :param target: the target image to draw on
    :param r:      the distance of the line to the lower left corner
    :param theta:  the angle between the x-axis and the point on the line that
                   is closest to the origin"""
    # the longest line can never be larger than the image itself
    infinity = target.shape[0] + target.shape[1]

    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    x_closest_to_origin = cos_theta * dist_to_origin
    y_closest_to_origin = sin_theta * dist_to_origin

    # startpoint of line
    x_start = int(x_closest_to_origin + infinity*(-sin_theta))
    y_start = int(y_closest_to_origin + infinity*(cos_theta))

    # endpoint of line
    x_stop = int(x_closest_to_origin - infinity*(-sin_theta))
    y_stop = int(y_closest_to_origin - infinity*(cos_theta))

    # cv2.line draws a line in target from the point (x_start, y_start)
    # to (x_stop, y_stop).
    # (0, 0, 255) denotes the colour of the line to be
    # drawn. In this case, it is red.
    cv2.line(target, (x_start, y_start), (x_stop, y_stop), (0, 0, 255), 2)


def draw_lines(target, lines):
    """Draw all lines on the target image."""
    for line in lines:
        r, theta = line[0]
        draw_line(target, r, theta)


img_with_lines = img.copy()
draw_lines(img_with_lines, lines)


# %%
# Write the lines
# All the changes made in the input image are finally
# written on a new image output.jpg
cv2.imwrite('output.jpg', img_with_lines)


# %%
# filter out horizontal lines
def remove_horizontal_lines(lines):
    result = []
    for line in lines:
        _, theta = line[0]
        if theta < (3 / 8) * np.pi or theta > (5 / 8) * np.pi:
            result.append(line)
    return result

print(lines)
vertical_lines = remove_horizontal_lines(lines)
img_with_lines = img.copy()
draw_lines(img_with_lines, vertical_lines)
cv2.imwrite('output_vertical.jpg', img_with_lines)


# %%
