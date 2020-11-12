from categorization import *
import os


def main():
    py_folder = os.path.dirname(os.path.abspath(__file__))
    while True:
        txt_folder = input("분류할 txt 파일이 있는 폴더 이름을 입력하세요 : ")
        txt_folder = f"{py_folder}\\{txt_folder}"
        if os.path.isdir(txt_folder) is False:
            print("폴더가 존재하지 않습니다.")
        else:
            break

    file_list = os.listdir(txt_folder)  # 파일 이름을 리스트로 저장.

    if not file_list:
        print("폴더에 파일이 존재하지 않습니다.")
        return

    print("명사 추출 중...")
    doc = noun_extractor(txt_folder)  # 문서의 명사를 추출하는 함수 수행
    print("명사 추출 완료...")

    print("빈도 추출 중...")
    frequency = frequency_extractor(doc)  # 각 단어의 빈도 행렬 추출 후 반환.
    print("빈도 추출 완료.")

    print("군집화 준비 중...")
    matrix = two_dimension_matrix(frequency)  # 빈도 리스트를 각 문서끼리 비교하여 2차원 유사도 행렬로 반환.
    print("군집화 준비 완료.")

    while True:
        try:
            category = int(input(f"몇 개의 카테고리로 분류할까요?(1 ~ {len(matrix)}) : "))
            if category <= len(matrix):
                break
            print("다시 입력해주세요.")
        except:
            print("숫자를 입력해주세요")

    print("군집화 수행 중...")
    # 계층적 군집화 알고리즘을 수행하고, n개의 계층으로 분리.
    clustering_result = hierarchical_clustering(matrix, category)
    print("군집화 완료.")

    while True:
        after = input("분류한 파일을 저장할 새로운 폴더의 이름을 입력해주세요 : ")
        if os.path.isdir(f"{py_folder}\\{after}"):
            print("이미 존재하는 폴더입니다. 다른 이름을 입력해주세요.")
        else:
            break

    print("파일 이동 중...")
    move_sorted_file(file_list, txt_folder, py_folder, after, clustering_result)  # 분류된 파일을 지정 폴더로 옮김.
    print("파일 이동 완료.")


main()
