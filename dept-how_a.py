import pyrealsense2 as rs
import numpy as np
import cv2

class DepthCamera:
    def __init__(self):
        self.pipe = rs.pipeline()
        cfg = rs.config()
        cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.pipe.start(cfg)

    def get_data(self):
        frames = self.pipe.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            return None

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        depth_scale = self.pipe.get_active_profile().get_device().first_depth_sensor().get_depth_scale()
        depth_image_meters = depth_image * depth_scale

        x, y = 320, 240
        distance = depth_image_meters[y, x]

        mask = np.where(depth_image_meters < 0.5, 255, 0).astype(np.uint8)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            if M['m00'] != 0:
                centroid_x = int(M['m10'] / M['m00'])
                centroid_y = int(M['m01'] / M['m00'])
                classification = self.classify_distance(distance)

                return classification, centroid_x, centroid_y, distance

        return None



    @staticmethod
    def classify_distance(distance):
        if 0.30 <= distance <= 0.32:
            return "xl"
        elif 0.34 <= distance <= 0.38:
            return "l"
        elif 0.43 <= distance <= 0.45:
            return "m"
        elif 0.47 <= distance <= 0.49:
            return "s"
        else:
            return "unknown"

    def stop(self):
        self.pipe.stop()


