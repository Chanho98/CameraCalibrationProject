# CameraCalibrationProject
카메라 센서의 오차를 바로잡는 Camera Calibration 실습

## 1.1. Camera Calibration 이란?
카메라로 촬영할 시 이미지는 렌즈, 이미지와 렌즈 사이의 거리, 카메라가 이루는 각도등의 요인에 의해서 영향을 받는다. 카메라 캘리브레이션은 
3차원을 2차원 이미지로 변환하는 과정에서 발생하는, 왜곡을 줄이고 개선하는 과정이다.
## 1.2. 렌즈계 왜곡 종류
렌즈 왜곡에는 크게 방사왜곡과 접선왜곡이 있다. 이중  방사왜곡은 볼록렌즈의 굴절률에 의한 것으로 렌즈 중심에서 부터의  거리에 의해 결정된다. 
<p align="center"><img src="https://user-images.githubusercontent.com/78125194/211782685-c1c3f335-af44-48a8-b706-73a82ceea2f0.png" width="600" height="400"/></p>
접선 왜곡은 카메라 렌즈와 이미지 센서의 수평이 맞지 않거나  또는 렌즈 자체의 Centering이 잘 맞지 않아서 생각하는  왜곡으로 타원형 형태의 왜곡 분포가 나타난다.
<p align="center"><img src="https://user-images.githubusercontent.com/78125194/211782959-8195ec0e-eb93-4b44-98d0-4921af574ca9.png" width="600" height="400"/></p>

****
## 2.1. Edge Detecting
체스판에서 코너를 찾고 코너 좌표를 반환하는 findChessboardCorners 함수 이용
```
ret, corners = cv2.findChessboardCorners(gray, (width, height), None)
```
원본 이미지와 코너 위치를 가져와서 원래 위치의 작은 이웃내에서 가장 좋은 코너 위치를 찾는다. 
```
cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
```
<p align="center"><img src="https://user-images.githubusercontent.com/78125194/211762176-7704973d-6609-4f0a-b28e-4e78b64a412d.png" width="600" height="400"/></p>

<p align="center"><img src="https://user-images.githubusercontent.com/78125194/211762190-87bf7de6-020c-410a-ad91-38a9a6363b8b.png" width="600" height="400"/></p>

## 2.2. cv2.calibrateCamera 함수이용
cv2.calibrateCamera 함수를 이용해서 Object points, Image points를 통해 왜곡 계소, 회전/변환 벡터를 리턴한다.
```
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
```

## 2.3. Undistortion
cv2.getOptimalNewCameraMatrix 함수를 이용하여, free scaling 파라미터에 기반 카메라 매트릭스를 수정할 수 있다. Alpha Parameter는  1에 가까울 수록 왜곡을 펼 때 잘라낸 부분들을 더 보여주고 펴진 부분 위조로 보고 싶다면 0에 가까운 인자를 주면 된다.
```
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

```

****
## 3.1. 실험 결과
### Before Calibration
<p align="center"><img src="https://user-images.githubusercontent.com/78125194/211768324-b890dc0d-dc83-405f-bd28-8f475efe3d62.jpg" width="600" height="400"/></p>

### After Calibration
<p align="center"><img src="https://user-images.githubusercontent.com/78125194/211768348-2d0aab25-150f-4ba9-bb5d-4aeb1333e709.png" width="600" height="400"/></p>

## 3.2. Re-Projection Error
 투영된 지점과 측정된 지점 사이의 거리만큼의 오차로, 3D 포인트의 추정치가 얼마나 정확한지를 측정하는 측도
 ```
 for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
    tot_error += error
 ```
![오차값](https://user-images.githubusercontent.com/78125194/211769001-efabdf44-c00e-4e08-ab4f-5b9e84508293.png)
****

## ○ 참고 문서
* [카메라 캘리브레이션 이론](https://darkpgmr.tistory.com/32) 참고
* [OpenCV 카메라 캘리브레이션 이론](https://foss4g.tistory.com/1665) 참고
* [OpenCV Camera Calibration 재투사 오차](https://leechamin.tistory.com/345) 참고
* [OpenCV 참조 git hub](https://github.com/opencv/opencv/tree/master)
