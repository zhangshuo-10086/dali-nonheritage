# core/symmetry.py
import cv2
import numpy as np

def calc_vertical_symmetry(img_gray: np.ndarray) -> float:
    h, w = img_gray.shape
    mid = w // 2
    left = img_gray[:, :mid]
    right = img_gray[:, mid:]
    right_flip = cv2.flip(right, 1)
    min_w = min(left.shape[1], right_flip.shape[1])
    left = left[:, :min_w]
    right_flip = right_flip[:, :min_w]
    diff = np.abs(left.astype(float) - right_flip.astype(float))
    avg_diff = np.mean(diff)
    score = 100 - (avg_diff / 255 * 100)
    return round(score,2)

def calc_horizontal_symmetry(img_gray: np.ndarray) -> float:
    h, w = img_gray.shape
    mid = h // 2
    top = img_gray[:mid, :]
    bottom = img_gray[mid:, :]
    bottom_flip = cv2.flip(bottom, 0)
    min_h = min(top.shape[0], bottom_flip.shape[0])
    top = top[:min_h, :]
    bottom_flip = bottom_flip[:min_h, :]
    diff = np.abs(top.astype(float) - bottom_flip.astype(float))
    avg_diff = np.mean(diff)
    score = 100 - (avg_diff / 255 * 100)
    return round(score,2)

def calc_rotate180_symmetry(img_gray: np.ndarray) -> float:
    rot_img = cv2.rotate(img_gray, cv2.ROTATE_180)
    diff = np.abs(img_gray.astype(float) - rot_img.astype(float))
    avg_diff = np.mean(diff)
    score = 100 - (avg_diff / 255 * 100)
    return round(score,2)
