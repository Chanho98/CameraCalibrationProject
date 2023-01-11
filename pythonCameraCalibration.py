import numpy as np
import cv2
import glob


# 종료기준 설정
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

height = 6
width = 8

# object points(3D) 준비, ex) (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((height * width, 3), np.float32)
objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)

# 이미지 파일로부터 object points, image points 저장을 위한 배열 생성
objpoints = [] # 실제 세계에서의 3D 점 위치
imgpoints = [] # 평면위의 이미지 점 위치.

# 이미지 불러오기
images = glob.glob('*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 체스판 이미지에서 코너 찾기 함수이용
    ret, corners = cv2.findChessboardCorners(gray, (width, height), None)

    # 발견하면 object points, image points에 추가
    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # 코너 확인
        img = cv2.drawChessboardCorners(img, (width, height), corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(500)

# camera calibration 함수 사용
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

# 왜곡 제거
img = cv2.imread('left12.jpg')
h,  w = img.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

# undistort 함수 사용
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv2.imwrite('calibresult.png', dst)

cv2.destroyAllWindows()

tot_error = 0

# Re-projection Error
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
    tot_error += error

print("total error: ", tot_error/len(objpoints))