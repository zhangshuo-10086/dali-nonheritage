import numpy as np

def box_counting_fractal_dim(binary_img:np.ndarray)->float:
    if len(binary_img.shape)!=2:
        return 0.0
    h, w = binary_img.shape
    if h <8 or w <8:
        return 0.0

    sizes = []
    counts = []
    for size in range(2, min(h,w)//2, 2):
        cnt = 0
        for i in range(0, h - size, size):
            for j in range(0, w - size, size):
                patch = binary_img[i:i+size, j:j+size]
                if np.sum(patch) > 0:
                    cnt +=1
        if cnt>0:
            sizes.append(size)
            counts.append(cnt)

    # 样本不足直接返回0
    if len(sizes)<3:
        return 0.0

    try:
        log_size = np.log10(sizes)
        log_cnt = np.log10(counts)
        p = np.polyfit(log_size, log_cnt, 1)
        D = -p[0]
    except Exception:
        return 0.0

    # 分形维合理区间限制：0~3，超出视为无效返回0
    D = np.clip(D, 0.0,3.0)
    return round(D,3)
