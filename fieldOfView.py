__author__ = 'clipo'

import os
import commands
import math

def compute_fov2(altitude,focal_length):
    focal_length_multiplier=1.6
    film_width = 36
    film_height = 24
    ## units are all meters
    ## convert distance to mm
    altitude *=  1000


    ## Account for focal length multiplier (actually, a film/sensor size multiplier)
    film_width = film_width/focal_length_multiplier
    film_height = film_height/focal_length_multiplier
    film_diag = (math.sqrt((film_width * film_width) + (film_height * film_height)))

    half_fov_h = (math.atan(film_width / (2 * focal_length)))
    fov_h = 2 * (altitude * math.tan(half_fov_h))

    half_fov_v = (math.atan(film_height / (2 * focal_length)))
    fov_v = 2 * (altitude * math.tan(half_fov_v))

    half_fov_d = (math.atan(film_diag / (2 * focal_length)))
    fov_d = 2 * (altitude * math.tan(half_fov_d))

    ##convert answer (currently in mm) back to meters
    fov_h = fov_h /1000
    fov_v = fov_v /1000
    fov_d = fov_d /1000

    return fov_h, fov_v, fov_d
