import numpy as np
import cv2
from PIL import Image, ImageEnhance, ImageOps

# 간단한 배경 제거 함수 구현 (임계값 기반)
def remove_background(image, threshold=240):
    """Simple background removal based on color threshold"""
    img_array = np.array(image)
    
    # RGB 이미지를 처리
    if len(img_array.shape) == 3 and img_array.shape[2] == 3:
        # 밝은 배경 픽셀 마스크 생성
        mask = np.all(img_array > threshold, axis=2)
        
        # RGBA 이미지 생성 (알파 채널 포함)
        rgba = np.zeros((img_array.shape[0], img_array.shape[1], 4), dtype=np.uint8)
        rgba[:, :, :3] = img_array
        rgba[:, :, 3] = np.where(mask, 0, 255)  # 배경은 투명하게, 객체는 불투명하게
        
        return Image.fromarray(rgba)
    return image

# 이미지 크기 조정 함수
def resize_image(image, size):
    """Resize an image to the specified size"""
    image = image.resize(size)
    return np.array(image)

# 이미지 회전 함수 - 짤림 방지를 위해 expand=True 추가
def rotate_image(image, angle):
    """Rotate an image by the given angle"""
    return image.rotate(angle, expand=True, resample=Image.BICUBIC)

# 이미지 좌우 반전 함수
def flip_image_horizontal(image):
    """Flip an image horizontally"""
    return ImageOps.mirror(image)

# 이미지 밝기 조정 함수
def adjust_brightness(image, factor):
    """Adjust the brightness of an image"""
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

# 이미지 대비 조정 함수
def adjust_contrast(image, factor):
    """Adjust the contrast of an image"""
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

# 이미지 색상 조정 함수
def adjust_color(image, factor):
    """Adjust the color saturation of an image"""
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)

# 이미지 선명도 조정 함수
def adjust_sharpness(image, factor):
    """Adjust the sharpness of an image"""
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)