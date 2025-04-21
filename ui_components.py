import streamlit as st

# 유사도 측정 방식에 대한 설명 함수
def show_metric_explanation():
    st.markdown("## 💡 유사도 측정 방식 설명")
    
    st.markdown("### 1. SSIM (Structural Similarity Index Measure)")
    st.markdown("""
    SSIM은 이미지의 구조적 유사성을 측정하는 지표입니다. 인간의 시각 시스템이 이미지의 구조적 정보에 민감하다는 점에 착안해 개발되었습니다.
    
    - **범위**: 0% (완전히 다름) ~ 100% (동일함)
    - **특징**: 밝기, 대비, 구조의 변화를 고려하여 계산
    - **활용**: 이미지 압축, 화질 평가 등에 주로 사용
    """)
    
    st.markdown("### 2. PSNR (Peak Signal-to-Noise Ratio)")
    st.markdown("""
    PSNR은 원본 이미지와 처리된 이미지 간의 픽셀 차이를 기반으로 한 품질 측정 지표입니다. 두 이미지 간의 '오차'를 측정합니다.
    
    - **원리**: MSE(평균 제곱 오차)를 기반으로 계산
    - **단위**: dB (데시벨) - 높을수록 유사도가 높음
    - **특징**: 픽셀 단위의 차이를 정량적으로 표현
    - **한계**: 인간의 시각적 인식과 항상 일치하지 않음
    """)
    
    st.markdown("### 3. VGG16 기반 코사인 유사도")
    st.markdown("""
    딥러닝 모델(VGG16)을 사용하여 이미지의 고수준 특징을 추출한 후, 그 특징 벡터 간의 코사인 유사도를 계산합니다.
    
    - **원리**: 사전 학습된 CNN 모델이 인식하는 이미지 특징의 유사성 측정
    - **범위**: 0% (완전히 다름) ~ 100% (동일함)
    - **특징**: 색상, 질감, 물체 등 이미지의 의미적 내용 비교 가능
    - **장점**: 인간의 시각적 인식과 더 유사한 결과를 제공하는 경향이 있음
    """)

# 슬라이더와 에디트 박스 조합 컴포넌트
def slider_with_input(label, min_val, max_val, default_val, step, key):
    col1, col2 = st.columns([7, 3])
    with col1:
        slider_value = st.slider(label, min_val, max_val, default_val, step, key=f"slider_{key}")
    with col2:
        input_value = st.number_input("", min_val, max_val, slider_value, step, key=f"input_{key}", label_visibility="collapsed")
        
    # 슬라이더와 입력 값 동기화
    if input_value != slider_value:
        return input_value
    return slider_value

# 결과 시각화 함수
def display_similarity_results(ssim_score, psnr_score, vgg_score, avg_score):
    # 결과 출력
    st.markdown("## 📊 유사도 비교 결과")
    
    # 표 형식으로 결과 표시
    results_df = {
        "비교 방식": ["SSIM", "PSNR", "VGG16 기반 Cosine 유사도"],
        "유사도 점수 (%)": [f"{ssim_score:.2f}%", f"{psnr_score:.2f}%", f"{vgg_score:.2f}%"]
    }
    st.table(results_df)
    
    # 시각적 게이지로 결과 표시
    st.markdown("### 시각적 유사도 표시")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**SSIM**: {ssim_score:.2f}%")
        st.progress(float(min(ssim_score/100, 1.0)))
        if ssim_score > 80:
            st.success("매우 유사한 구조")
        elif ssim_score > 60:
            st.info("유사한 구조")
        else:
            st.warning("구조적 차이가 큼")
        
    with col2:
        st.markdown(f"**PSNR**: {psnr_score:.2f}%")
        st.progress(float(min(psnr_score/100, 1.0)))
        if psnr_score > 80:
            st.success("매우 유사한 품질")
        elif psnr_score > 60:
            st.info("양호한 품질")
        else:
            st.warning("품질 차이가 큼")
        
    with col3:
        st.markdown(f"**VGG16 기반 Cosine 유사도**: {vgg_score:.2f}%")
        st.progress(float(min(vgg_score/100, 1.0)))
        if vgg_score > 80:
            st.success("매우 유사한 의미적 내용")
        elif vgg_score > 60:
            st.info("유사한 의미적 내용")
        else:
            st.warning("의미적 차이가 큼")
    
    # 평균 점수 표시
    st.markdown(f"**평균 유사도 점수**: {avg_score:.2f}%")
    st.progress(float(min(avg_score/100, 1.0)))
    if avg_score > 80:
        st.success("전반적으로 매우 유사")
    elif avg_score > 60:
        st.info("전반적으로 유사")
    else:
        st.warning("전반적으로 차이가 큼")