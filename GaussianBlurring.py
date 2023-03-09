#모든 픽셀에 똑같은 가중치를 부여했던 평균 블러링과 달리 가우시안 블러링은 마스크 중심 원소에
#높은 가중치를 부여한다.

#openCV 에서는 가우시안 블러링을 위해 GaussianBlur 함수를 제공한다.
#세 번째 아규먼트를 0 으로 하면 지정한 커널 크기에 맞추어 시그마를 계산해서 사용한다.

#평균 블러링 결과 이미지는 에지를 포함해서 전체적으로 이미지가 흐리게 되지만
#가우시안 블러링 결과 이미지는 에지가 선명히 보이는 상태에서 블러링이 이루어진다.
#가우시안 블러링은 보통 에지 검출 전 노이즈를 제거하기 위해서 사용하는 기법이다.


import cv2 as cv

img = cv.imread('imgs/dcgallery.PNG')
img_averblur = cv.blur(img, (5,5))
img_gaussianblur = cv.GaussianBlur(img, (5,5), 0)

cv.imshow('Original', img)
cv.imshow('averResult', img_averblur)
cv.imshow('gaussianReslut', img_gaussianblur)

cv.waitKey(0)
cv.destroyAllWindows()