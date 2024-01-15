import pyrealsense2 as rs
import numpy as np
import cv2
import socket

def look_vision():
    pipe = rs.pipeline()
    cfg = rs.config()

    cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    pipe.start(cfg)

    while True:
        frame = pipe.wait_for_frames()
        depth_frame = frame.get_depth_frame()
        color_frame = frame.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        depth_cm = cv2.applyColorMap(cv2.convertScaleAbs(depth_image,
                                                         alpha=0.5), cv2.COLORMAP_JET)

        gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

        #cv2.imshow('rgb', color_image)
        cv2.imshow('depth', depth_cm)

        if cv2.waitKey(1) == ord('q'):
            break

    pipe.stop()
    cv2.destroyAllWindows()


# Function to classify distance
def classify_distance(distance):
    if 0.30 <= distance <= 0.33:
        return "xl"
    elif 0.34 <= distance <= 0.38:
        return "l"
    elif 0.43 <= distance <= 0.46:
        return "m"
    elif 0.47 <= distance <= 0.50:
        return "s"
    else:
        return "unknown"

def run_vision():
    pipe = rs.pipeline()
    cfg = rs.config()

    cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    pipe.start(cfg)
    while True:
        frames = pipe.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        depth_scale = pipe.get_active_profile().get_device().first_depth_sensor().get_depth_scale()
        depth_image_meters = depth_image * depth_scale

        x, y = 320, 280

        distance = depth_image_meters[y, x]

        mask = np.where(depth_image_meters < 0.5, 255, 0).astype(np.uint8)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)

            M = cv2.moments(largest_contour)
            if M['m00'] != 0:
                centroid_x = int(M['m10'] / M['m00'])
                centroid_y = int(M['m01'] / M['m00'])

                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.5), cv2.COLORMAP_JET)
                depth_colormap = cv2.bitwise_and(depth_colormap, depth_colormap, mask=mask)

                depth_colormap = cv2.circle(depth_colormap, (centroid_x, centroid_y), 5, (255, 0, 255), -1)

                depth_colormap = cv2.circle(depth_colormap, (320, 280), 5, (0, 255, 0), -1)

                # Display the classification result
                classification = classify_distance(distance)
                print(f"Classification: {classification}")

                print(centroid_x)
                print(centroid_y)

        print(f"Distance to pixel ({x},{y}): {distance} meters")

        #cv2.imshow('Color', color_image)
        cv2.imshow('vision', depth_colormap)

        if cv2.waitKey(1) == ord('q'):
            break


    pipe.stop()
    cv2.destroyAllWindows()


if __name__ == '__main__':
     run_vision()

# import pyrealsense2 as rs
# import numpy as np
# import cv2
#
#
# # Function to classify distance
# def classify_distance(distance):
#     if 0.30 <= distance <= 0.32:
#         return "large"
#     elif 0.43 <= distance <= 0.45:
#         return "medium"
#     elif 0.47 <= distance <= 0.49:
#         return "small"
#     else:
#         return "unknown"
#
#
# def run_vision():
#     pipe = rs.pipeline()
#     cfg = rs.config()
#
#     cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
#     cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#
#     pipe.start(cfg)
#
#     align = rs.align(rs.stream.color)
#
#     while True:
#         frames = pipe.wait_for_frames()
#         aligned_frames = align.process(frames)
#
#         depth_frame = aligned_frames.get_depth_frame()
#         color_frame = aligned_frames.get_color_frame()
#
#         if not depth_frame or not color_frame:
#             continue
#
#         depth_image = np.asanyarray(depth_frame.get_data())
#         color_image = np.asanyarray(color_frame.get_data())
#
#         depth_scale = pipe.get_active_profile().get_device().first_depth_sensor().get_depth_scale()
#         depth_image_meters = depth_image * depth_scale
#
#         x, y = 320, 240
#
#         distance = depth_image_meters[y, x]
#
#         mask = np.where(depth_image_meters < 0.5, 255, 0).astype(np.uint8)
#
#         contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#         if contours:
#             largest_contour = max(contours, key=cv2.contourArea)
#
#             M = cv2.moments(largest_contour)
#             if M['m00'] != 0:
#                 centroid_x = int(M['m10'] / M['m00'])
#                 centroid_y = int(M['m01'] / M['m00'])
#
#                 depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.5), cv2.COLORMAP_JET)
#                 depth_colormap = cv2.bitwise_and(depth_colormap, depth_colormap, mask=mask)
#
#                 depth_colormap = cv2.circle(depth_colormap, (centroid_x, centroid_y), 5, (255, 0, 255), -1)
#
#                 # Display the classification result
#                 classification = classify_distance(distance)
#                 print(f"Classification: {classification}")
#
#                 print(centroid_x)
#                 print(centroid_y)
#
#         print(f"Distance to pixel ({x},{y}): {distance} meters")
#
#         # cv2.imshow('Color', color_image)
#         cv2.imshow('vision', depth_colormap)
#
#         if cv2.waitKey(1) == ord('q'):
#             break
#
#     pipe.stop()
#     cv2.destroyAllWindows()
#
# if __name__ == '__main__':
#     run_vision()
