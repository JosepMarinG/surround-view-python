This repository is a modified version of the project [surround-view-system-introduction]([url](https://github.com/neozhaoliang/surround-view-system-introduction)).

It includes:

    YAML calibration files for the MiniCERNBot with USB fisheye cameras.

    A new script that publishes the generated surround view image on a ROS 2 topic.

    A clear explanation of the workflow (since the original repo lacks proper documentation).

📷 Hardware Setup:
<img width="1966" height="830" alt="image" src="https://github.com/user-attachments/assets/699254bf-71af-4173-be39-3c38b85b3fe2" />
This image shows the MiniCERNBot with a Nuc and 4 USB fisheye cameras.

🔧Here is an explanation of the repo:
run_calibrate_camera.py calibrates the camera with a nice UI.

    python3 run_calibrate_camera.py   -i 2   --grid 11x8   --resolution 1920x1080   -framestep 10   -o yaml/cam2.yaml   --fisheye   --no_gst
<img width="924" height="694" alt="image" src="https://github.com/user-attachments/assets/00d3e733-b85b-4b76-a929-5d13b348e527" />


run_get_projection_maps.py gets the perspective. Change the data on the param_settings.py file inside the surround_view folder before runing the projection script.
The order of seleccion of the points is very important. First the top left, top right, bottom left, bottom right.

    python3 run_get_projection_maps.py -camera front

<img width="1564" height="1033" alt="image" src="https://github.com/user-attachments/assets/dee16eb9-3c7c-46a4-a793-4bbcd9186904" />
<img width="1572" height="588" alt="image" src="https://github.com/user-attachments/assets/99a06b52-19a0-44c6-aaf9-0ae058278bb2" />
This images show how the points should be clicked and the demo result.
<img width="635" height="846" alt="image" src="https://github.com/user-attachments/assets/bafc0226-0478-45e3-adec-9bd634d88872" />
This shows a calibration pattern used for the perspective setup of the MiniCERNBot.





The projection script uses an image saved in the folder images with the name front.png, back.png... To obtain this images a script was created called take_picture.py

In param_settings the variables to change according to the calibration pattern you use are the following (everything is in pixels):
shift_w = how far away the birdview looks outside of the calibration pattern horizontaly
shift_h = how far away the birdview looks outside of the calibration pattern verticaly
inn_shift_w = size of the gap between the calibration pattern and the robot horizontaly
inn_shift_h = size of the gap between the calibration pattern and the robot verticaly
total_w = Total width of the whole picture
total_h = Total height of the whole picture
xl = horizontal component of the top left point of the robot image
xr = horizontal component of the bottom right point of the robot image
yt = vertical component of the top left point of the robot image
yb = vertical component of the bottom right point of the robot image
project_keypoints = pixel locations of the four points to be chosen when running the projection script

<img width="1372" height="1120" alt="image" src="https://github.com/user-attachments/assets/2621ff3d-eab1-4d26-addb-27c3ecdaa699" />

✅ Results

<img width="1685" height="941" alt="image" src="https://github.com/user-attachments/assets/fb699c29-1d08-41ab-8ca3-d141fe2e11ef" />
<img width="1718" height="933" alt="image" src="https://github.com/user-attachments/assets/92264f4d-b77c-4062-8091-f4701d18d084" />
<img width="1670" height="938" alt="image" src="https://github.com/user-attachments/assets/a09dc8a8-3285-4abc-9dcc-580cf341f334" />


⚠️ Performance Consideration

The original Python implementation was too slow for real-time use. To overcome this, we explored a C++ alternative already available at:
👉 https://github.com/JokerEyeAdas/AdasSourrondView/tree/main

Our improved fork of this C++ implementation can continuously generate and publish the surround view in a ROS 2 topic:
👉 https://github.com/JosepMarinG/SourrondViewC-


