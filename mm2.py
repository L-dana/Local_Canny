import os, sys
import random
import numpy as np
import cv2 as cv

#img returned [h,w,3]
def read_image(src):
    img_array = np.fromfile(src, np.uint8)
    img = cv.imdecode(img_array, cv.IMREAD_COLOR)

    return img


def write_image(dst, img, params=None):
    try:
        ext = os.path.splitext(dst)[1]
        result, n = cv.imencode(ext, img, params)


        if result:
            with open(dst, mode='w+b') as f:
                n.tofile(f)
            return True

        else:
            return False

    except Exception as e:

        print(e)
        return False


# Function to remove background
def get_canny_and_mask(img):

    #트랙바를 조정할 때마다 실행되는 콜백함수
    #이곳에 트랙바로 조정할 openCV 함수를 넣을 수 있다.
    #지금은 아무 동작이 없는 더미로 정의
    def on_trackbar(x):
        pass

    h, w, c = img.shape
    print(h , w, c)

    if (h >= 900) or (w >= 1600):
        h = int(h/1.7)
        w = int(h/1.7)

    elif (h <= 200) or (w <= 200):
        h = h*2
        w = w*2

    #namedWindow 함수를 사용하여 트랙바를 붙인 윈도우를 생성해야 합니다.
    cv.namedWindow('Canny', cv.WINDOW_NORMAL)
    cv.resizeWindow("Canny", h, w)

    #트랙바를 생성한다.
    #트랙바 이름, 윈도우 이름, 트랙바의 최소값, 트랙바의 최댓값, 콜백함수를 입력
    cv.createTrackbar('low threshold', 'Canny', 0, 100, on_trackbar)
    cv.createTrackbar('high threshold', 'Canny', 0, 500, on_trackbar)

    #트랙바의 초기값을 설정해줍니다.
    #트랙바 이름, 트랙바가 붙은 윈도우 이름으로 트랙바에 접근.
    cv.setTrackbarPos('low threshold', 'Canny', 50)
    cv.setTrackbarPos('high threshold', 'Canny' , 150)

    #이미지를 그레이 스케일로 변환
    #Canny 함수는 그레이 스케일로 입력해야 한다.
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img_mask = np.zeros((img.shape[0], img.shape[1], 1), dtype =np.uint8)

    #트랙바가 조정 시 Canny함수에 반영되도록 루프를 사용한다.
    while(1):
    
        #현재 트랙바의 위치를 가져온다.
        low = cv.getTrackbarPos('low threshold', 'Canny')
        high = cv.getTrackbarPos('low threshold', 'Canny')

        #트랙바로부터 가져온 값으로 Canny함수의 파라미터를 조정
        img_canny = cv.Canny(img_gray, low, high)


        #Canny 함수의 실행 결과를 화면에 보여준다.
        cv.imshow('Canny', img_canny)

        #ESC 키를 누르면 루프를 종료
        key = cv.waitKey(10)
        if key == 27:
            write_image(ns[0] + '_canny.png', ~img_canny) #캐니반환

            ## 외곽선 검출
            kernal = cv.getStructuringElement(cv.MORPH_RECT, (3,3)) 
            tmp = cv.dilate(img_canny, kernal, iterations = 3) #흰색 영역 부풀리기 3회
            tmp = cv.erode(tmp, kernal, iterations= 3) #흰색 영역 세번 깎기
            contours, hh = cv.findContours(tmp, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_TC89_KCOS)
            cc = len(contours)
            print(cc)

            idx = 0
            while idx >= 0:
                #c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                cv.drawContours(img_mask, contours, idx, (255,255,255), -1, cv.LINE_AA, hh) ##외곽선 그리기(내부 채움)
                '''
                cv.drawContours(img_mask, contours, contourIdx, color, thickness=None, lineType=None, hierarchy=None, maxLevel=None, offest=None)

                contours: findContours() 함수로 구한 외곽선 좌표 정보
                contourIdx: 그릴 외곽선 번호. 음수(-1)로 지정하면 모든 외곽선을 그림
                color: 외곽선 색상
                thickness: 외곽선 두께. 음수(-1)로 지정하면 내부를 채움
                lineType: LINE_4, LINE_8, LINE_AA 중 하나 지정
                hierarchy: 외곽선 계층 정보
                maxLevel: 그리기를 수행할 최대 외곽선 레벨. 0이면 contourIdx로 지정된 외곽선만 그림
                offset: 오프셋(이동 변위). 지정한 좌표 크기만큼 외곽선 좌표를 이동하여 그림
                '''
                idx = hh[0, idx, 0]  # 다음 외곽선이 없으면 -1 반환

            write_image(ns[0] + '_mask.png', img_mask) #내부가 채워진 외곽선 반환(마스크 이미지가 됨)
            break

    #cv.destroyAllWindows()
    cv.destroyWindow('Canny')
    return img_canny, img_mask



def rmbg_fn(img):
    _, mask = get_canny_and_mask(img)
    object = cv.copyTo (img , mask)
    background = cv.copyTo (img , ~mask)
    #img = np.concatenate([img, mask], axis=2, dtype=np.uint8)
    #mask = mask.repeat(3, axis=2)

    write_image(ns[0] + '_object.png', object)
    write_image(ns[0] + '_background.png', background)
    


def apply(src):
    print("abgremoving on ", src)

    img_tar = read_image(src)  ##읽고
    rmbg_fn(img_tar)  ##처리
    #cv.add(img_tar, mask)


if __name__ == "__main__":
    input_list = sys.argv
    
    if len(input_list) <= 1:
        input('파일을 드래그 드랍해')

    src_list = input_list[1:]

    for src in src_list:
        ns = src.split(".")

        print(ns)
        result = apply(src) ## 프로세싱


    print("끝!")
    input('press enter to quit')