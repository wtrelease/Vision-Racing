import cv2

def convert_to_bw(name):
    im_gray = cv2.imread('maps/images/'+ name + '.png', 0)
    im_bw = cv2.threshold(im_gray, 80, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite('maps/b&w/'+ name +'.png', im_bw)
