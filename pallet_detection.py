import pyrealsense2 as rs
import numpy as np
import cv2

def pallet(corner_x, corner_y, angle):
    print(f"Corner coordinate of mapped area: ({corner_x}, {corner_y}), Orientation Angle: {angle}")

pipe = rs.pipeline()
cfg = rs.config()

cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

pipe.start(cfg)

# Set the depth range for pallet detection (in meters)
min_depth = 0.95
max_depth = 1.08

while True:
    # Wait for a coherent pair of frames: depth and color
    frames = pipe.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    if not depth_frame or not color_frame:
        continue

    # Convert images to numpy arrays
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    # Convert depth frame to meters (assuming depth_units is in meters)
    depth_scale = pipe.get_active_profile().get_device().first_depth_sensor().get_depth_scale()
    depth_image_meters = depth_image * depth_scale

    # Create an empty depth colormap
    depth_colormap = np.zeros_like(color_image)

    # Create a mask for distances within the specified depth range
    mask = np.where((depth_image_meters >= min_depth) & (depth_image_meters <= max_depth), 255, 0).astype(np.uint8)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour (assuming it's the region within the specified depth range)
        largest_contour = max(contours, key=cv2.contourArea)

        # Get the rotated bounding box of the largest contour
        rect = cv2.minAreaRect(largest_contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # Choose one of the corners (let's use the top-left corner)
        corner_x, corner_y = box[1]

        # Calculate the orientation angle of the pallet
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

        pallet(corner_x, corner_y, angle)

    # Display the frames
    cv2.imshow('Color', color_image)
    cv2.imshow('Depth', depth_colormap)

    if cv2.waitKey(1) == ord('q'):
        break

# Stop streaming
pipe.stop()
cv2.destroyAllWindows()
