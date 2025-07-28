import os
import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from surround_view import CaptureThread, CameraProcessingThread
from surround_view import FisheyeCameraModel, BirdView
from surround_view import MultiBufferManager, ProjectedImageBuffer
import surround_view.param_settings as settings


def main():
    rclpy.init()
    node = rclpy.create_node("birdview_publisher")
    publisher = node.create_publisher(Image, "/birdview/image_raw", 10)
    bridge = CvBridge()

    # Configuración de cámaras
    yamls_dir = os.path.join(os.getcwd(), "yaml")
    camera_ids = [2, 6, 4, 0]
    flip_methods = [0, 2, 0, 2]
    names = settings.camera_names
    cameras_files = [os.path.join(yamls_dir, name + ".yaml") for name in names]
    camera_models = [FisheyeCameraModel(f, name) for f, name in zip(cameras_files, names)]

    # Captura
    capture_tds = [CaptureThread(cid, flip, use_gst=False)
                   for cid, flip in zip(camera_ids, flip_methods)]
    capture_buffer_manager = MultiBufferManager()
    for td in capture_tds:
        capture_buffer_manager.bind_thread(td, buffer_size=8)
        if td.connect_camera():
            td.start()

    # Procesado
    proc_buffer_manager = ProjectedImageBuffer()
    process_tds = [CameraProcessingThread(capture_buffer_manager, cid, model)
                   for cid, model in zip(camera_ids, camera_models)]
    for td in process_tds:
        proc_buffer_manager.bind_thread(td)
        td.start()

    # BirdView
    birdview = BirdView(proc_buffer_manager)
    birdview.load_weights_and_masks("./weights.png", "./masks.png")
    birdview.start()

    try:
        while rclpy.ok():
            img = birdview.get()
            msg = bridge.cv2_to_imgmsg(img, encoding="bgr8")
            publisher.publish(msg)

            rclpy.spin_once(node, timeout_sec=0.01)

            print("birdview fps: {}".format(birdview.stat_data.average_fps), end="\r")

    except KeyboardInterrupt:
        pass

    finally:
        print("\nShutting down...")

        # Detener threads
        for td in process_tds:
            td.stop()
        for td in capture_tds:
            td.stop()
            td.disconnect_camera()

        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
