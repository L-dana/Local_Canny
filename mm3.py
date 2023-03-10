import os, sys
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
def CLAHE(img):

   
    #한번에 비교해보기 위해서 크기를 줄임
    #img = cv.resize(img, ((w//2, h//2))) 
    cv.imshow('source', img)


    #RGB 이미지를 Lab 색상 공간으로 변환
    #원래  Hunter 1948 Lab 색 공간을 가리켰으나, 현대에 들어 CIE 1976 L*a*b* 색 공간을 가리키게 되었다.
    #L*a*b* 색 공간은 RGB나 CMYK가 표현할 수 있는 모든 색역을 포함, 인간이 지각할 수 없는 색깔도 포함하고 있음
    #장점은 RGB나 CMYK와 달리 매체에 독립적이라는 것이다. 
    #장비나 인쇄 매체에 따라 색이 달라지지 않고, 인간의 시각에 대한 연구를 바탕으로 정의되었다.

    #L 값은 밝기를 나타낸다. L = 0 이면 검은색이며, L = 100 이면 흰색
    #a 는 빨강과 초록 중 어느쪽인지 나타낸다 a 이 - 이면 초록이고, + 이면 빨강/보라 쪽으로 치우친 색
    #b 는 노랑과 파랑을 나타낸다. b 이 - 이면 파랑이고 b 이 + 이면 노랑

    #RGB 및 CMYK 색 공간은 매체에 독립적이지 않기 때문에, 
    #위의 색 공간 방식을 L*a*b* 색 공간으로 변환하려면 먼저 sRGB나 어도비 RGB 등의 절대 색 공간으로 변환해야 한다.
    lab = cv.cvtColor(img, cv.COLOR_BGR2LAB)

    #CLAHE 개체 생성
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

    #채널 분할(밝기, 빨강/초록, 노랑/파랑)
    l,a,b = cv.split(lab)

    #적용(밝기 기준으로 'Concrast' 제한된 적응형 히스토그램 평활화)
    l = clahe.apply(l)

    #채널 합체, 다시 RGB이미지로
    lab = cv.merge((l,a,b))
    out1 = cv.cvtColor(lab, cv.COLOR_LAB2BGR)
    write_image(ns[0] + '_lab.png', out1)
    #cv.imshow('lab', out1)



    #RGB 이미지를 HSV색 공간 이미지로 변환
    #색상 Hue, 채도 Saturation , 명도 Value
    #비슷한 것으로 HSL(Lightness), HSI(Intensity) 등

    #H는 가시광선 스펙트럼을 고리 모양으로 배치했을 때 (빨강을 0°로) 상대적인 배치 각도를 의미
    #따라서 H 값은 0°~360°의 범위를 갖고 360°와 0°는 같은 색상 빨강을 가리킨다.
    #S는 색의 가장 진한 상태를 100%로 하였을 때 진함의 정도를 나타낸다. 채도값 0%는 같은 명도의 무채색을 나타낸다.
    #V는 흰색, 검은색 제외한 색 100%, 검은색을 0%로 하였을 때 밝은 정도를 나타낸다.
    hsv= cv.cvtColor(img, cv.COLOR_BGR2HSV)

    #CLAHE 개체 생성
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

    #채널 분할(색상, 채도, 명도)
    h,s,v = cv.split(hsv)

    #적용(명도 기준 'Concrast' 제한된 적응형 히스토그램 평활화)
    v = clahe.apply(v)

    #채널 합체, 다시 RGB이미지로
    ycbcr = cv.merge((h,s,v))
    out2 = cv.cvtColor(ycbcr, cv.COLOR_HSV2BGR)
    write_image(ns[0] + '_hsv.png', out2)


    #RGB 이미지를 YUV색 공간으로 변환
    #가장 직관적이며 일반적인것이 RGB지만, 데이터가 너무 많고 처리하기 버겁다. 따라서 YUB가 고안되었다.
    #인간이 민감한 휘도(밝기)성분과 상대적으로 덜 민감한 색상 성분으로 분리한다

    #Y 는 밝기, U = (파랑색 - 밝기), V = (빨강색 - 밝기)

    #전송방식에 따라 YCbCr 또는 YPrPb로 나눈다
    #수학적으로는 동일하나 YPbPr 아날로그 방식, YCbCr은 디지털
    #실생활에서 사용하는것은 디지털개념적인 YCbCr이며 YUV와는 엄밀히 따지면 차이가 있지만 유사하며, 
    #혼용해서 사용하는 경우가 많다. (보통YUV = YCbCr)
    yuv= cv.cvtColor(img, cv.COLOR_BGR2YUV)

    #CLAHE 개체 생성
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

    #채널 분할(밝기, 파랑-밝기, 빨강-밝기)
    y,u,v = cv.split(yuv)

    #적용(밝기 기준 'Concrast' 제한된 적응형 히스토그램 평활화)
    y = clahe.apply(y)

    #채널 합체, 다시 RGB이미지로
    yuv = cv.merge((y,u,v))
    out3 = cv.cvtColor(yuv, cv.COLOR_YUV2BGR)
    write_image(ns[0] + '_yuv.png', out3)

    cv.waitKey()
    cv.destroyWindow('source')



def app(src):
    print("색상, 밝기 보정", src)

    img_tar = read_image(src)  ##읽고
    CLAHE(img_tar)  ##색 공간별로 보정 먹이고 저장.



if __name__ == "__main__":
    input_list = sys.argv
    
    if len(input_list) <= 1:
        input('파일을 드래그 드랍해')

    src_list = input_list[1:]

    for src in src_list:
        ns = src.split(".")

        print(ns)
        app(src) ## 프로세싱

    print("끝!")
    input('press enter to quit')