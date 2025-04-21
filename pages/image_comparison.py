import streamlit as st
import uuid
from PIL import Image
import sys
import os

# 현재 디렉토리를 상위 폴더로 변경
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 상대 경로로 import (수정된 부분)
from image_processing import (
    resize_image, rotate_image, flip_image_horizontal, remove_background,
    adjust_brightness, adjust_contrast, adjust_color, adjust_sharpness
)
from similarity_metrics import compare_ssim, compare_psnr, compare_vgg_cosine
from ui_components import slider_with_input, display_similarity_results
from db_utils import save_results

def app():  # 이 함수가 올바르게 정의되어야 합니다
    st.title("이미지 유사도 비교 도구")
    
    # 이미지 업로드 받기
    st.markdown("## 📸 이미지 업로드")
    img1 = st.file_uploader("실제 사진 업로드", type=["jpg", "png", "jpeg"])
    img2 = st.file_uploader("AI 생성 사진 업로드", type=["jpg", "png", "jpeg"])

    # 두 이미지가 모두 업로드된 경우 비교 진행
    if img1 and img2:
        image1 = Image.open(img1).convert("RGB")
        image2 = Image.open(img2).convert("RGB")
        
        # 이미지 원본 정보 표시
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"실제 사진 크기: {image1.width} x {image1.height}")
        with col2:
            st.write(f"AI 생성 사진 크기: {image2.width} x {image2.height}")
        
        # 이미지 편집 기능 추가
        st.markdown("## 🖌️ 이미지 편집")
        
        # 탭으로 각 이미지 편집 섹션 분리
        tab1, tab2 = st.tabs(["실제 사진 편집", "AI 생성 사진 편집"])
        
        with tab1:
            st.subheader("실제 사진 편집")
            
            # 배경 제거 옵션
            remove_bg1 = st.checkbox("배경 제거", key="remove_bg1")
            if remove_bg1:
                try:
                    with st.spinner("배경을 제거하는 중..."):
                        image1 = remove_background(image1)
                    st.success("배경이 제거되었습니다!")
                except Exception as e:
                    st.error(f"배경 제거 중 오류가 발생했습니다: {str(e)}")
            
            # 좌우반전 옵션
            flip1 = st.checkbox("좌우반전", key="flip1")
            if flip1:
                image1 = flip_image_horizontal(image1)
            
            # 회전 옵션 (슬라이더 + 에디트 박스)
            rotation1 = slider_with_input("회전 각도", -180, 180, 0, 1, "rot1")
            if rotation1 != 0:
                image1 = rotate_image(image1, rotation1)
            
            # 밝기 조정 (슬라이더 + 에디트 박스)
            brightness1 = slider_with_input("밝기 조정", 0.0, 3.0, 1.0, 0.05, "bright1")
            if brightness1 != 1.0:
                image1 = adjust_brightness(image1, brightness1)
            
            # 대비 조정 (슬라이더 + 에디트 박스)
            contrast1 = slider_with_input("대비 조정", 0.0, 3.0, 1.0, 0.05, "contrast1")
            if contrast1 != 1.0:
                image1 = adjust_contrast(image1, contrast1)
            
            # 색상 조정 (슬라이더 + 에디트 박스)
            color1 = slider_with_input("색상 조정", 0.0, 3.0, 1.0, 0.05, "color1")
            if color1 != 1.0:
                image1 = adjust_color(image1, color1)
            
            # 선명도 조정 (슬라이더 + 에디트 박스)
            sharpness1 = slider_with_input("선명도 조정", 0.0, 3.0, 1.0, 0.05, "sharp1")
            if sharpness1 != 1.0:
                image1 = adjust_sharpness(image1, sharpness1)
                
            # 조정값 일괄 적용 섹션
            st.write("---")
            st.subheader("조정값 직접 입력")
            col1, col2, col3 = st.columns(3)
            with col1:
                custom_rotation1 = st.number_input("회전 각도 값", -180, 180, rotation1, 1, key="custom_rot1")
            with col2:
                custom_brightness1 = st.number_input("밝기 값", 0.0, 3.0, brightness1, 0.05, key="custom_bright1")
            with col3:
                custom_contrast1 = st.number_input("대비 값", 0.0, 3.0, contrast1, 0.05, key="custom_contrast1")
            
            col1, col2 = st.columns(2)
            with col1:
                custom_color1 = st.number_input("색상 값", 0.0, 3.0, color1, 0.05, key="custom_color1")
            with col2:
                custom_sharpness1 = st.number_input("선명도 값", 0.0, 3.0, sharpness1, 0.05, key="custom_sharp1")
            
            if st.button("조정값 일괄 적용", key="apply_custom1"):
                # 조정값 적용
                image1_original = Image.open(img1).convert("RGB")
                
                # 배경 제거 (일괄 적용 시에도 배경 제거 옵션이 켜져 있으면 적용)
                if remove_bg1:
                    try:
                        with st.spinner("배경을 제거하는 중..."):
                            image1_original = remove_background(image1_original)
                    except Exception as e:
                        st.error(f"배경 제거 중 오류가 발생했습니다: {str(e)}")
                
                # 좌우반전
                if flip1:
                    image1_original = flip_image_horizontal(image1_original)
                    
                # 다른 조정 적용
                image1 = rotate_image(image1_original, custom_rotation1)
                image1 = adjust_brightness(image1, custom_brightness1)
                image1 = adjust_contrast(image1, custom_contrast1)
                image1 = adjust_color(image1, custom_color1)
                image1 = adjust_sharpness(image1, custom_sharpness1)
                
                st.success("조정값이 일괄 적용되었습니다.")
                
            st.image(image1, caption="편집된 실제 사진", use_column_width=True)
        
        with tab2:
            st.subheader("AI 생성 사진 편집")
            
            # 배경 제거 옵션
            remove_bg2 = st.checkbox("배경 제거", key="remove_bg2")
            if remove_bg2:
                try:
                    with st.spinner("배경을 제거하는 중..."):
                        image2 = remove_background(image2)
                    st.success("배경이 제거되었습니다!")
                except Exception as e:
                    st.error(f"배경 제거 중 오류가 발생했습니다: {str(e)}")
            
            # 좌우반전 옵션
            flip2 = st.checkbox("좌우반전", key="flip2")
            if flip2:
                image2 = flip_image_horizontal(image2)
            
            # 회전 옵션 (슬라이더 + 에디트 박스)
            rotation2 = slider_with_input("회전 각도", -180, 180, 0, 1, "rot2")
            if rotation2 != 0:
                image2 = rotate_image(image2, rotation2)
            
            # 밝기 조정 (슬라이더 + 에디트 박스)
            brightness2 = slider_with_input("밝기 조정", 0.0, 3.0, 1.0, 0.05, "bright2")
            if brightness2 != 1.0:
                image2 = adjust_brightness(image2, brightness2)
            
            # 대비 조정 (슬라이더 + 에디트 박스)
            contrast2 = slider_with_input("대비 조정", 0.0, 3.0, 1.0, 0.05, "contrast2")
            if contrast2 != 1.0:
                image2 = adjust_contrast(image2, contrast2)
            
            # 색상 조정 (슬라이더 + 에디트 박스)
            color2 = slider_with_input("색상 조정", 0.0, 3.0, 1.0, 0.05, "color2")
            if color2 != 1.0:
                image2 = adjust_color(image2, color2)
            
            # 선명도 조정 (슬라이더 + 에디트 박스)
            sharpness2 = slider_with_input("선명도 조정", 0.0, 3.0, 1.0, 0.05, "sharp2")
            if sharpness2 != 1.0:
                image2 = adjust_sharpness(image2, sharpness2)
                
            # 조정값 일괄 적용 섹션
            st.write("---")
            st.subheader("조정값 직접 입력")
            col1, col2, col3 = st.columns(3)
            with col1:
                custom_rotation2 = st.number_input("회전 각도 값", -180, 180, rotation2, 1, key="custom_rot2")
            with col2:
                custom_brightness2 = st.number_input("밝기 값", 0.0, 3.0, brightness2, 0.05, key="custom_bright2")
            with col3:
                custom_contrast2 = st.number_input("대비 값", 0.0, 3.0, contrast2, 0.05, key="custom_contrast2")
            
            col1, col2 = st.columns(2)
            with col1:
                custom_color2 = st.number_input("색상 값", 0.0, 3.0, color2, 0.05, key="custom_color2")
            with col2:
                custom_sharpness2 = st.number_input("선명도 값", 0.0, 3.0, sharpness2, 0.05, key="custom_sharp2")
            
            if st.button("조정값 일괄 적용", key="apply_custom2"):
                # 조정값 적용
                image2_original = Image.open(img2).convert("RGB")
                
                # 배경 제거 (일괄 적용 시에도 배경 제거 옵션이 켜져 있으면 적용)
                if remove_bg2:
                    try:
                        with st.spinner("배경을 제거하는 중..."):
                            image2_original = remove_background(image2_original)
                    except Exception as e:
                        st.error(f"배경 제거 중 오류가 발생했습니다: {str(e)}")
                
                # 좌우반전
                if flip2:
                    image2_original = flip_image_horizontal(image2_original)
                    
                # 다른 조정 적용
                image2 = rotate_image(image2_original, custom_rotation2)
                image2 = adjust_brightness(image2, custom_brightness2)
                image2 = adjust_contrast(image2, custom_contrast2)
                image2 = adjust_color(image2, custom_color2)
                image2 = adjust_sharpness(image2, custom_sharpness2)
                
                st.success("조정값이 일괄 적용되었습니다.")
                
            st.image(image2, caption="편집된 AI 생성 사진", use_column_width=True)
        
        # 이미지 비교 섹션
        st.markdown("## 🔍 이미지 비교")
        
        # 두 이미지 비교 보기
        st.image([image1, image2], caption=["편집된 실제 사진", "편집된 AI 생성 사진"], width=300)

        # 이미지 크기 설정에서 이미지 리사이즈
        image_size = st.session_state.get('image_size', (256, 256))
        resized1 = resize_image(image1, image_size)
        resized2 = resize_image(image2, image_size)

        # 유사도 계산 버튼
        if st.button("유사도 계산하기"):
            with st.spinner("유사도를 계산 중입니다..."):
                # 고유 ID 생성
                result_id = str(uuid.uuid4())
                
                # 이미지 저장
                real_image_filename = f"Result/real_{result_id}.png"
                ai_image_filename = f"Result/ai_{result_id}.png"
                
                # PIL 이미지 저장
                image1.save(real_image_filename)
                image2.save(ai_image_filename)
                
                # 유사도 계산
                ssim_score = compare_ssim(resized1, resized2)
                psnr_score = compare_psnr(resized1, resized2)
                vgg_score = compare_vgg_cosine(image1, image2)
                avg_score = (ssim_score + psnr_score + vgg_score) / 3
                
                # 결과를 DB에 저장
                saved_id = save_results(
                    real_image_filename, 
                    ai_image_filename, 
                    ssim_score, 
                    psnr_score, 
                    vgg_score, 
                    avg_score
                )

                # 결과 표시
                display_similarity_results(ssim_score, psnr_score, vgg_score, avg_score)
                st.success(f"결과가 저장되었습니다. 결과 ID: {saved_id}")
    else:
        st.info("이미지 비교를 시작하려면 두 장의 이미지를 업로드해주세요.")