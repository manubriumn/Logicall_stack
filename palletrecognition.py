import cv2
import glob
from stack_pictures import stack

def adjust_brightness(image, brightness=0):
    if brightness != 0:
        adjusted = cv2.convertScaleAbs(image, beta=brightness)
        return adjusted
    return image

def find_rectangles(canny_image, min_area=100):
    contours, _ = cv2.findContours(canny_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rectangles = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(approx) == 4 and cv2.contourArea(approx) > min_area:
            rectangles.append(approx)
    return rectangles

def draw_rectangles(image, rectangles):
    for rectangle in rectangles:
        cv2.drawContours(image, [rectangle], -1, (0, 255, 0), 2)
    return image

def display_images(folder_path, min_area=100):
    image_files = glob.glob(folder_path + '/*.jpg') + glob.glob(folder_path + '/*.png') + glob.glob(folder_path + '/*.jpeg') + glob.glob(folder_path + '/*.gif')
    images = []

    for image_path in image_files:
        img = cv2.imread(image_path)
        baw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(baw, (15, 13), 0)
        canny = cv2.Canny(blur, 20, 60)
        rectangles = find_rectangles(canny, min_area)
        img_with_rectangles = draw_rectangles(img.copy(), rectangles)
        images.append([img, canny, img_with_rectangles])
    stacked_images = stack(0.5, images)
    cv2.imshow('Alle Afbeeldingen', stacked_images)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

folder_path = "C:/Minor SMR/opdracht semester 2/code/Pallet pictures"
display_images(folder_path, min_area = 2500)  # Pas de minimale oppervlakte hier aan
