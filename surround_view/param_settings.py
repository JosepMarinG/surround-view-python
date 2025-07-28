import os
import cv2

 
camera_names = ["front", "back", "left", "right"]

# --------------------------------------------------------------------
# (shift_width, shift_height): how far away the birdview looks outside
# of the calibration pattern in horizontal and vertical directions
shift_w = 300
shift_h = 200

# size of the gap between the calibration pattern and the car
# in horizontal and vertical directionsmake_luminance_balance() ajusta el brillo entre pares de cámaras en zonas solapadas para que no haya diferencias abruptas de color o luz. Por ejemplo
inn_shift_w = 115
inn_shift_h = 100

# total width/height of the stitched image
total_w = 800 + 2 * shift_w
total_h = 1000 + 2 * shift_h

# four corners of the rectangular region occupied by the car
# top-left (x_left, y_top), bottom-right (x_right, y_bottom)
xl = shift_w + 135 + inn_shift_w
xr = total_w - xl
yt = shift_h + 135 + inn_shift_h
yb = total_h - yt
# --------------------------------------------------------------------

project_shapes = {
    "front": (total_w, yt),
    "back":  (total_w, yt),
    "left":  (total_h, xl),
    "right": (total_h, xl)
}

# pixel locations of the four points to be chosen.
# you must click these pixels in the same order when running
# the get_projection_map.py script
project_keypoints = {
    "front": [(shift_w + 135, shift_h),
              (shift_w + 665, shift_h),
              (shift_w + 135, shift_h + 135),
              (shift_w + 665, shift_h + 135)],

    "back":  [(shift_w + 135, shift_h),
              (shift_w + 665, shift_h),
              (shift_w + 135, shift_h + 135),
              (shift_w + 665, shift_h + 135)],

    "left":  [(shift_h + 330, shift_w),
              (shift_h + 670, shift_w),
              (shift_h + 330, shift_w + 135),
              (shift_h + 670, shift_w + 135)],

    "right": [(shift_h + 330, shift_w),
              (shift_h + 670, shift_w),
              (shift_h + 330, shift_w + 135),
              (shift_h + 670, shift_w + 135)]
}

car_image = cv2.imread(os.path.join(os.getcwd(), "images", "car.png"))
car_image = cv2.resize(car_image, (xr - xl, yb - yt))
