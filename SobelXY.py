#에지는 픽셀값이 급격히 변화하는 지점이다.
#1차원 그래프로 그리면 픽셀값이 갑자기 커지는(기울기가 큰) 부분을 말한다.

#에지는 미분을 사용하여 구한다. 주변보다 1차 미분값이 큰 부분을 에지로 검출하게 된다.
#구체적인 과정은 아래와 같다.

#1차 미분의 근사값을 계산하기 위해서 미리 정의한 마스크와 이미지를 컨볼루션 한다.
#G(x) =  ┏ -1 0 +1 ┓	G(y) = ┏ -1 -2 -1 ┓
#		     ┃ -2 0 +2 ┃		        ┃  0  0  0 ┃
#		     ┗ -1 0 +1 ┛		     ┗ +1 +2 +1 ┛
#마스크 G(x) 는 x축 상에서의 에지를 검출한다.
#마스크 G(y) 는 y축 상에서의 에지를 검출한다.


#Sobel(입력이미지, 출력 타입, x방향 미분 차수, y방향 미분 차수, 커널 크기)
#출력타입에 -1을 입력하면 입력과 같은 타입으로 나옴.
#커널(마스크) 크기 기본은 3
#x, y 방향 미분 차수를  0으로 하면 해당 방향은 연산하지 않는다.

#Sobel(img, CV_64F, 1, 0, 3)
#img에 x방향 마스크로 컨볼루션 하여 64F로 출력하여 img_result 에 입력한다. 마스크 크기는 3x3

#에지 검출(Sobel 함수 시햄 후)후 convertScaleAbs() 함수를 사용하여 결과에 절대값을 적용하고
#값 범위를 8비트 usigned int 로 변경해줘야 윈도우에서 결과를 볼 수 있다.


#소벨 마스크 G(x)의 결과와 G(y) 의 결과를 합치면 x와 y방향의 엣지를 모두 얻을수있다.



import cv2 as cv

#img_color = cv.imread('imgs/box.png', cv.IMREAD_COLOR)
img_color = cv.imread('imgs/white circle.png', cv.IMREAD_COLOR)
img_gray = cv.cvtColor(img_color, cv.COLOR_BGR2GRAY)

img_sobel_x = cv.Sobel(img_gray, cv.CV_64F, 1, 0, ksize=3)
#Sobel(입력이미지, 출력 타입, x방향 미분 차수, y방향 미분 차수, 커널 크기)
img_sobel_x = cv.convertScaleAbs(img_sobel_x)
#소벨처리 후 결과에 절대값을 적용하고 값 범위를 8비트로 변경해주어야 윈도우에서 결과를 볼 수 있다.

img_sobel_y = cv.Sobel(img_gray, cv.CV_64F, 0, 1, ksize=3)
img_sobel_y = cv.convertScaleAbs(img_sobel_y)

img_sobel = cv.addWeighted(img_sobel_x, 1, img_sobel_y, 1, 0)

cv.imshow('Sobel_x', img_sobel_x)
cv.imshow('Sobel_y', img_sobel_y)
cv.imshow('Sobel', img_sobel)

cv.waitKey(0)
cv.destroyAllWindows()