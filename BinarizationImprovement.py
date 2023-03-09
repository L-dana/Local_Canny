#Binarization 에서 이어짐.
#보통 원본 컬러 이미지를 그레이 스케일로 변환 후, 임계값을 기준으로 배경과 물체를 분리한다.

#그레이 스케일 이미지의 픽셀값을 검사해 픽셀값이 임계보다 크면 결과 이미지의 같은 위치 픽셀값을 255(흰색)
#으로 하고 픽셀값이 임계값보다 작으면 0(검은색) 으로 한다. 결과적으로 값이 0과 255의 두가지만 있는 바이너리 이미지가 나온다.

#바이너리 이미지에서 객체가 흰색이 되도록 조작해야 한다.
#이진화 이후 사용되는 openCV함수들이 처리 시 흰색 영역을 대상으로 설계되었기 때문이다.

#이진화를 위한 임계값을 정할 때 트랙바를 사용할 수 있다
#트랙바를 사용해 임계값을 찾은 후 threshold 함수를 위한 고정값으로 사용하면 된다.


import cv2 as cv
import sys

#트랙바를 위한 콜백함수
def on_trackbar(x):
    pass

#이미지를 읽어옵니다.
img_color = cv.imread('imgs/Screenshot_20220617-191333.png', cv.IMREAD_COLOR)
if img_color is None:
    print('이미지를 읽어 올 수 없습니다. ')
    sys.exit(1)

#그레이 스케일 이미지로 변환한다.
img_gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)
cv.imshow('Grayscale', img_gray)

#윈도우에 트랙바를 추가한다.
cv.namedWindow('Binary')
cv.createTrackbar('threshold', 'Binary', 0, 255, on_trackbar)
cv.setTrackbarPos('threshold', 'Binary', 127)


#트랙바를 사용하여 파라미터를 조정할 openCV 함수를 콜백함수에 넣는 대신 필요한 부분에 루프를 추가해 해결
while True:

    #트랙바의 값을 읽어와서 threshold 함수의 파라미터로 사용한다.
    thresh = cv.getTrackbarPos('threshold', 'Binary')

    #사용할 이미지에서 추출할 객체와 배경의 픽셀값에 따라서
	#THRESHOLD_BINAY 와 THRESHOLD_BINAY_INV 를 선택합니다. (선택할 객체만 흰색이 되도록)
    retval, img_binary = cv.threshold(img_gray, thresh, 255, cv.THRESH_BINARY)

    #결과 이미지를 보여준다.
    cv.imshow('Binary', img_binary)

    #ESC키를 누를 때 루프에서 나온다.
    if cv.waitKey(1) & 0xFF == 27:
        break