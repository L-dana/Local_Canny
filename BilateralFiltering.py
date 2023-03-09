#양방향 필터링 Bilateral Filtering
#에지를 보존하면서 노이즈를 감소시킬 수 있는 방법이다. 결과 이미지에서 질감이 있는 부분만 블러링되고
#에지 부분은 보전된다.

#그 결과로 대체로 비슷한 색의 노이즈는 제거되나 선명한 색대비를 보이는 노이즈는 그대로 남아버린다.



import cv2 as cv

img = cv.imread('imgs/iris2.png')
img_bilateral =cv.bilateralFilter(img, 9, 75, 75)


cv.imshow('Origianl', img)
cv.imshow('Result', img_bilateral)

cv.waitKey(0)
cv.destroyAllWindows()