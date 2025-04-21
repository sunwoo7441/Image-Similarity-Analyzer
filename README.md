# Image-Similarity-Analyzer
AI 생성 이미지와 실제 이미지의 유사도를 다양한 지표로 분석하는 도구

# AI 이미지 유사도 분석 도구

AI 생성 이미지와 실제 이미지 간의 유사도를 정량적으로 분석하고 시각화하는 종합 도구입니다.

## 주요 기능

- 다양한 이미지 유사도 평가 알고리즘 (SSIM, PSNR, VGG16) 활용
- 결과 저장 및 비교 조회 기능
- 그래프 및 통계를 통한 데이터 분석
- 코멘트 기능을 통한 정성적 평가 기록

## 설치 및 실행 방법

1. 필요 라이브러리 설치:
```bash
pip install -r requirements.txt


## 애플리케이션 실행:streamlit run app.py

## 사용 방법
유사도 비교: 실제 이미지와 AI 생성 이미지를 업로드하여 유사도 측정

결과 조회: 저장된 분석 결과 검색 및 조회
결과 요약: 전체 분석 결과의 통계 및 시각화 확인

## 분석 지표
SSIM (Structural Similarity Index): 이미지의 구조적 유사성 측정
PSNR (Peak Signal-to-Noise Ratio): 픽셀 단위 차이 정량화
VGG 기반 특징 유사도: 사전 학습된 VGG16 모델을 활용한 고수준 특징 비교
