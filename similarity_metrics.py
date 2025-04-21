import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from math import log10
from scipy.spatial.distance import cosine
import torch
from torchvision.models import vgg16, VGG16_Weights
from torchvision import transforms

# SSIM 비교 함수
def compare_ssim(img1, img2):
    gray1 = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2GRAY)
    gray2 = cv2.cvtColor(np.array(img2), cv2.COLOR_RGB2GRAY)
    score, _ = ssim(gray1, gray2, full=True)
    return float(score * 100)  # float32를 일반 float으로 변환

# PSNR 비교 함수 (MAX_PSNR을 기준으로 백분율 계산)
def compare_psnr(img1, img2):
    mse = np.mean((np.array(img1) - np.array(img2)) ** 2)
    if mse == 0:
        return 100.0
    psnr = 20 * log10(255.0 / np.sqrt(mse))
    # PSNR을 백분율로 변환 (50dB를 100%로 가정)
    MAX_PSNR = 50.0
    percentage = min(psnr / MAX_PSNR * 100, 100)
    return float(percentage)  # numpy 타입을 일반 float으로 변환

# VGG16 기반 Cosine 유사도 비교 함수 (PyTorch 사용)
def compare_vgg_cosine(img1, img2):
    # Load pretrained model
    model = vgg16(weights=VGG16_Weights.IMAGENET1K_V1)
    model.eval()
    # Remove the classifier to get features only
    model = torch.nn.Sequential(*list(model.children())[:-1])
    
    # Preprocessing
    preprocess = transforms.Compose([
        transforms.Resize(224),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    # Process images
    img1_tensor = preprocess(img1).unsqueeze(0)
    img2_tensor = preprocess(img2).unsqueeze(0)
    
    # Get features
    with torch.no_grad():
        feat1 = model(img1_tensor).flatten().numpy()
        feat2 = model(img2_tensor).flatten().numpy()
    
    return float((1 - cosine(feat1, feat2)) * 100)  # numpy 타입을 일반 float으로 변환