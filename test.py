import cv2 as cv

if __name__ == "__main__":
    #input_list = sys.argv
    #if len(input_list) <= 1:

        #input('파일을 드래그 드랍해')

    #src_list = input_list[1:]
    i = cv.imread('imgs/roffjrtlvhfem.PNG', cv.IMREAD_GRAYSCALE)
    cv.imshow("dd", i)
    cv.waitKey()



    print("끝!")
    #input('press enter to quit')