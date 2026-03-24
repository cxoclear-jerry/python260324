import os
import shutil
from pathlib import Path

# 다운로드 폴더 경로
DOWNLOADS_PATH = Path("C:/Users/student/Downloads")

# 파일 분류 규칙 정의
FILE_RULES = {
    "images": [".jpg", ".jpeg"],
    "data": [".csv", ".xlsx"],
    "docs": [".txt", ".doc", ".pdf"],
    "archive": [".zip"]
}


def create_directories():
    """필요한 폴더가 없으면 생성"""
    for folder_name in FILE_RULES.keys():
        folder_path = DOWNLOADS_PATH / folder_name
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"생성됨: {folder_path}")


def classify_and_move_files():
    """파일을 분류하여 해당 폴더로 이동"""
    
    if not DOWNLOADS_PATH.exists():
        print(f"오류: {DOWNLOADS_PATH} 경로가 존재하지 않습니다.")
        return
    
    # 모든 파일에 대해 처리
    for file_path in DOWNLOADS_PATH.glob("*"):
        # 파일만 처리 (폴더는 제외)
        if not file_path.is_file():
            continue
        
        # 파일 확장자 확인
        file_ext = file_path.suffix.lower()
        
        # 분류 규칙에 맞는 폴더 찾기
        for folder_name, extensions in FILE_RULES.items():
            if file_ext in extensions:
                destination_folder = DOWNLOADS_PATH / folder_name
                destination_path = destination_folder / file_path.name
                
                try:
                    shutil.move(str(file_path), str(destination_path))
                    print(f"이동됨: {file_path.name} → {folder_name}/")
                except Exception as e:
                    print(f"오류 ({file_path.name}): {e}")
                break


def main():
    """메인 함수"""
    print("="*50)
    print("다운로드 폴더 파일 자동 분류 시작")
    print("="*50)
    
    # 1단계: 필요한 폴더 생성
    print("\n[1단계] 필요한 폴더 생성...")
    create_directories()
    
    # 2단계: 파일 분류 및 이동
    print("\n[2단계] 파일 분류 및 이동...")
    classify_and_move_files()
    
    print("\n" + "="*50)
    print("파일 분류 완료!")
    print("="*50)


if __name__ == "__main__":
    main()
