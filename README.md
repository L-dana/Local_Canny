# Local_Canny
Canny Edge Detector


#mm.py 
캐니만 땁니다.

#mm2.py
캐니 따고, 외곽선 검출해서 내부 채운 다음 마스크 땁니다.
이후 마스크에 따라서 배경과 물체를 분리

#mm3.py
색이나 밝기가 한쪽으로 치우쳐져 있어서 캐니가 제대로 안 될 경우
색과 밝기를 보정합니다. 부작용으로 이미지 화질이 약간 저하될 수 있음.
색 공간별로 보정을 먹인 다음 뽑아줍니다.
