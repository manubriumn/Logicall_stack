import pyrealsense2 as rs
import numpy as np
import cv2
import socket
import threading
import time

status = 0

# Function to classify distance
def classify_distance(distance):

    if 0.30 <= distance <= 0.32:

        return "large"

    elif 0.43 <= distance <= 0.45:

        return "medium"

    elif 0.47 <= distance <= 0.49:

        return "small"

    else:
        return "unknown"


# Function to move the robot based on classification
def move_robot(sock, classification):
    global status
    try:
        if classification == "small" :
            sock.sendall(b"set_digital_output(1, OFF)")
            time.sleep(1)
            sock.sendall(b"movel(posx(559.0, -56.8, 300.1, 169.3, 180.0, -10.7), v=60, a=60)")
            time.sleep(1)
            status = 1
            print(f"stattt: {status}")
        if status == 1:
            sock.sendall(b"set_digital_output(1, ON)")
            time.sleep(1)
            sock.sendall(b"movel(posx(559.0, -56.8, 650.1, 169.3, 180.0, -10.7), v=40, a=40)")
            time.sleep(1)
            sock.sendall(b"set_digital_output(1, OFF)")

        if classification == "medium":
            sock.sendall(b"movel(posx(659.0, -56.8, 300.1, 169.3, 180.0, -10.7), v=40, a=40)")
            time.sleep(1)
            status = 2
            print(f"stattt: {status}")
        if status == 2 :
            sock.sendall(b"movel(posx(559.0, -56.8, 661.1, 169.3, 180.0, -10.7), v=60, a=60)")
            
        else:
            print("Unknown classification")
    except Exception as e:
        print(f"Error moving the robot: {e}")

# Function to handle vision processing
def vision_thread(sock):
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

                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.5), cv2.COLORMAP_JET)
                depth_colormap = cv2.bitwise_and(depth_colormap, depth_colormap, mask=mask)

                depth_colormap = cv2.circle(depth_colormap, (centroid_x, centroid_y), 5, (255, 0, 255), -1)

                # Display the classification result
                classification = classify_distance(distance)
                print(f"Classification: {classification}")

                print(centroid_x)
                print(centroid_y)

                move_robot(sock, classification)

        print(f"Distance to pixel ({x},{y}): {distance} meters")

        cv2.imshow('Color', color_image)
        cv2.imshow('Depth', depth_colormap)

        if cv2.waitKey(1) == ord('q'):
            break

    pipe.stop()
    cv2.destroyAllWindows()

# Function to handle robot control
def robot_thread():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the robot is listening
    robot_address = ('192.168.137.100', 9225)
    sock.connect(robot_address)

    try:
        sock.sendall(b"movel(posx(559.0, -56.8, 661.1, 169.3, 180.0, -10.7), v=60, a=60)")
    except Exception as e:
        print(f"Error initializing the robot: {e}")
    else:
        vision_thread(sock)

    sock.close()

# Create and start threads
robot_control_thread = threading.Thread(target=robot_thread)
robot_control_thread.start()

# Wait for the robot control thread to finish
robot_control_thread.join()
