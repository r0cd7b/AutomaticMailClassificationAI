from konlpy.tag import Okt
from numpy import dot
from numpy.linalg import norm
from sklearn.cluster import AgglomerativeClustering
import os
import shutil


def frequency_extractor(document):  # 빈도 행렬 추출 함수.
    noun = set()  # 세트(집합) 자료 구조 선언.
    for i in document:  # 명사 추출된 문서들의 수만큼 반복.
        for j in i:  # 각 문서들의 명사 수만큼 반복.
            noun.add(j)  # 각 문서들의 명사를 모두 세트(집합)에 추가.
    noun = list(noun)  # 세트(집합)을 이후 인덱스 연산에 활용하기 위해 리스트로 변경.

    # 문서의 수만큼 리스트 생성 후, 세트의 자료 수만큼 2차원 리스트 추가 생성.
    frequency = [[0 for i in range(len(noun))] for j in range(len(document))]

    for i in range(len(noun)):  # 세트의 자료 수만큼 반복.
        for j in range(len(document)):  # 각 문서의 수만큼 반복.
            frequency[j][i] = document[j].count(
                noun[i]
            )  # 문서 속 명사들과 세트 속 명사들을 비교하여 카운트.

    return frequency  # 빈도를 나타내는 말뭉치 반환.


def cos_similarity(a, b):  # 유사도 측정 함수, 유사도가 높으면 0, 낮으면 1을 반환한다.
    temp = norm(a) * norm(b)
    if temp > 0:  # 0으로 나눌 수 없으므로 temp 값이 0이면 최대값인 1을 반환한다.
        result = 1 - dot(a, b) / temp  # 만약 temp 값이 0이 아닌 경우, 계산하는 식.
    else:
        result = 1
    return result


def two_dimension_matrix(frequency):
    matrix = [
        [cos_similarity(frequency[i], frequency[j]) for i in range(len(frequency))]
        for j in range(len(frequency))
    ]
    return matrix


def hierarchical_clustering(matrix, n_clusters=2):  # 계층적 군집화 알고리즘 수행 함수.
    return AgglomerativeClustering(n_clusters).fit(matrix).labels_


def noun_extractor(txt_folder):
    okt = Okt()  # Twitter 클래스의 객체 선언.
    doc = []

    for root, dirs, files in os.walk(txt_folder):  # 폴더 안의 모든 문서를 불러옴.
        for fname in files:
            full_fname = os.path.join(root, fname)
            try:
                f = open(full_fname, "r", encoding="UTF-8")
                data = f.read()  # 각 문서의 모든 문자를 반환.
            except:
                f = open(full_fname, "r", encoding="ANSI")
                data = f.read()  # 각 문서의 모든 문자를 반환.
            doc.append(okt.nouns(data))  # 반환한 문자를 이용하여 토큰화 수행(명사 추출).
            f.close()

    return doc


def move_sorted_file(file_list, txt_folder, py_folder, after, clustering_result):  # 파일을 분류한대로 옮기는 함수.
    for i in range(len(file_list)):  # 전체 파일 수만큼 반복.
        before_dir = f"{txt_folder}\\{file_list[i]}"  # 분류 전 파일들의 폴더 경로.
        after_dir = f"{py_folder}\\{after}\\{clustering_result[i]}"  # 분류 이후 파일을 옮길 폴더의 경로.

        if not (os.path.isdir(after_dir)):  # 만약 존재하지 않는 경로일 경우.
            os.makedirs(os.path.join(after_dir))  # 경로 생성.

        after_dir = f"{after_dir}\\{file_list[i]}"  # 각 파일들의 경로.
        shutil.move(before_dir, after_dir)  # 파일을 옮기는 함수 수행.
