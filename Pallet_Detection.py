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

                return classification, centroid_x, centroid_y, distance, color_image, depth_image

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

    def get_pallet(self):
        frames = self.pipe.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        if not depth_frame:
            return None

        depth_image = np.asanyarray(depth_frame.get_data())
        depth_scale = self.pipe.get_active_profile().get_device().first_depth_sensor().get_depth_scale()
        depth_image_meters = depth_image * depth_scale

        mask = np.where((depth_image_meters >= 0.95) & (depth_image_meters <= 1.08), 255, 0).astype(np.uint8)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            rect = cv2.minAreaRect(largest_contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            corner_x, corner_y = box[1]
            angle = rect[2]

            # Apply the mask to the depth colormap
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.5), cv2.COLORMAP_JET)
            depth_colormap = cv2.bitwise_and(depth_colormap, depth_colormap, mask=mask)

            # Draw a circle at the corner on the depth colormap
            depth_colormap = cv2.circle(depth_colormap, (corner_x, corner_y), 5, (255, 0, 255), -1)

            # Draw a line to indicate the orientation of the pallet
            depth_colormap = cv2.drawContours(depth_colormap, [box], 0, (0, 255, 0), 2)

            # Further noise reduction by blurring
            kernel_size = (15, 15)  # Choose a valid odd kernel size
            depth_colormap = cv2.GaussianBlur(depth_colormap, kernel_size, 0)

            return corner_x, corner_y, angle, depth_colormap

        return None

    def stop(self):
        self.pipe.stop()


def main():
    # Create an instance of the DepthCamera class
    depth_camera = DepthCamera()

    while True:
        # Get data from the DepthCamera class
        data = depth_camera.get_data()
        pallet_data = depth_camera.get_pallet()

        if data:
            # Display the data or perform other processing here for Depth Camera
            classification, centroid_x, centroid_y, distance, color_image, depth_image = data
            cv2.putText(color_image, f"Class: {classification}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(color_image, f"Distance: {distance:.2f} meters", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)
            cv2.circle(color_image, (centroid_x, centroid_y), 5, (0, 255, 0), -1)
            cv2.imshow("Color Camera", color_image)

            # Print Depth Camera Data
            print(f"Depth Camera Data: ('{classification}', {centroid_x}, {centroid_y}, {distance})")

        if pallet_data:
            # Display the data or perform other processing here for Pallet Detector
            corner_x, corner_y, angle, depth_colormap = pallet_data
            cv2.imshow("Depth Colormap", depth_colormap)

            # Print Pallet Detector Data
            print(f"Pallet Detector Data: ({corner_x}, {corner_y}, {angle})")

        # Break the loop on 'q' key press
        if cv2.waitKey(1) == ord('q'):
            break

    # Stop streaming
    depth_camera.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

