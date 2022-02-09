import numpy as np
import json

from matplotlib import pyplot as plt
from skimage.io import imshow, show
from skimage.io import imread, imsave
from skimage.filters import median
from skimage.morphology import disk
from skimage.exposure import histogram


def get_params_from_json(path: str) -> dict:
    """Чтение из json-файла"""
    with open(path) as json_file:
        params = json.load(json_file)
    return params


def read_image(path: str) -> np.ndarray:
    """Чтение изображения из файла"""
    return imread(path)


def save_image(path: str, img: np.ndarray):
    """Запись изображения в файла"""
    imsave(path, img)


def get_median_image(img: np.ndarray, params: dict) -> np.ndarray:
    """Получение изображения """
    md = params['mode']  # паддинг изображения
    size: list = params['size']  # размер структурного элемента
    median_img = median(img, np.dstack((disk(size[0]),  # медианное преобразование
                                        disk(size[1]),
                                        disk(size[2]))), mode=md)
    return median_img


def create_histogram(img: np.ndarray):
    """Создание гистограммы и подготовка для отображения"""
    hist_red, bins_red = histogram(img[:, :, 2])  # гистограмма красного канала
    hist_green, bins_green = histogram(img[:, :, 1])  # гистограмма зелёного канала
    hist_blue, bins_blue = histogram(img[:, :, 0])  # гистограмма синего канала

    plt.ylabel('число отсчетов')
    plt.xlabel('значение яркости')
    plt.title('Гистограмма распределения яркостей по каждому каналу')
    plt.plot(bins_green, hist_green, color='green', linestyle='-', linewidth=1)
    plt.plot(bins_red, hist_red, color='red', linestyle='-', linewidth=1)
    plt.plot(bins_blue, hist_blue, color='blue', linestyle='-', linewidth=1)
    plt.legend(['green', 'red', 'blue'])


def main():
    params = get_params_from_json('settings.json')  # чтение параметров
    img = read_image(params['input'])  # чтение изображения
    m_img = get_median_image(img, params)  # преобразование
    save_image(params['output'], m_img)  # сохранение изображения

    # построение плота
    fig = plt.figure(figsize=(12, 6))
    fig.add_subplot(2, 2, 1)
    imshow(img)
    fig.add_subplot(2, 2, 2)
    imshow(m_img)
    fig.add_subplot(2, 2, 3)
    create_histogram(img)
    fig.add_subplot(2, 2, 4)
    create_histogram(m_img)
    show()


main()
