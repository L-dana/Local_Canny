#이진화(Binarization / Thresholding) 는 그레이 스케일 이미지를 바이너리 (Binary) 이미지로 변환하는 방법
#임계값(Threshold) 를 기준으로 그레이 스케일 이미지를 흰색 영역과 검은색 영역으로 분리
# 임계값이 127일 경우 입력 이미지에서 127 이하면 검은색(0) 127 초과이면 흰색(1) 로 바이너리 이미지 생성

#openCV 에서는 이미지 전체에 하나의 임계값을 사용하는 Threshold() 함수와
#이미지를 작은 영역으로 나눠 영역별로 다른 임계값을 사용하는 adaptiveThreshold() 함수를 제공


# Threshold() 함수를 통해 이미지 전체에 하나의 임계값을 사용하여 이진화를 함




import cv2 as cv
import sys

#이미지를 읽어온다.
img_color = cv.imread('imgs/Untitled-1_copy.jpg', cv.IMREAD_COLOR)
if img_color is None:
    print('이미지 파일을 읽을 수 없음. ')
    sys.exit(1)

#그레이 스케일 이미지로 변환한다.
img_gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)

#임계값 127을 사용하여 이진화를 함
#이진화 타입으로 THRESH_BINARY 를 사용하면
#픽셀값이 127 보다 크면 255, 127보다 작으면 0이 된다.
#이진화 타입으로 THRESH_BINARY_INV 를 사용하면 반대로 된다.
retval, img_binary = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY)
retval, img_binary_reflect = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY_INV)

#retval, img_binary = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY) << 에서
#앞부분 retval, 이 없으면 제대로 동작하지 않음.


#결과 이미지를 보여준다.
cv.imshow('Grayscale', img_gray)
cv.imshow('Binary', img_binary)
cv.imshow('Binary_reflect', img_binary_reflect)

cv.waitKey(0)