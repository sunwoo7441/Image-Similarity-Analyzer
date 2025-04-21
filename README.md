# Image-Similarity-Analyzer
AI 생성 이미지와 실제 이미지의 유사도를 다양한 지표로 분석하는 도구

애플리케이션 실행:streamlit run app.py

사용 방법
유사도 비교: 실제 이미지와 AI 생성 이미지를 업로드하여 유사도 측정
결과 조회: 저장된 분석 결과 검색 및 조회
결과 요약: 전체 분석 결과의 통계 및 시각화 확인
분석 지표
SSIM (Structural Similarity Index): 이미지의 구조적 유사성 측정
PSNR (Peak Signal-to-Noise Ratio): 픽셀 단위 차이 정량화
VGG 기반 특징 유사도: 사전 학습된 VGG16 모델을 활용한 고수준 특징 비교
