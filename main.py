import json

def run_json_mode():
    print("json 파일을 읽습니다")

    try:
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("오류: data.json 파일이 없습니다.")
    except json.JSONDecodeError:
        print("오류: JSON파일 형식이 잘못되었습니다.")
        return
    
    filters = data["filters"]
    patterns = data["patterns"]
    
    print("=== 필터 목록 ===")

    for size in filters:
        print(size, "필터 로드 완료")
    
    print("=== 패턴 MAC 분석 ===")
    
    total = 0
    passed = 0
    failed_cases = []

    for name, pattern_data in patterns.items():
        
        #1. 패턴 이름에서 크기 추출
        parts = name.split("_")
        size_key = "size_" + parts[1]
        
        #2. 필터 라벨 정규화
        current_filters = {}
        
        for label, filter_data in filters[size_key].items():
            standard_label = normalize_label(label)
            current_filters[standard_label] = filter_data
            
        cross_filter = current_filters["Cross"]
        x_filter = current_filters["X"]

        #3. 패턴의 숫자 배열 가져오기
        patterns = pattern_data["input"]
        expected = normalize_label(pattern_data["expected"])

        #4. MAC 점수 계산
        score_cross = calculate_mac(patterns, cross_filter)
        score_x = calculate_mac(patterns, x_filter)
        
        #5. 판정
        result = decide(score_cross, score_x)
        
        #6. 정답 비교
        total = total + 1
        
        if result == expected:
            passed = passed +1
            status = "PASS"
        else:
            status = "Fail"
            
            if result == "UNDECIDED":
                reason = "허용오차에 따른 동점"
            else: 
                reason = "판정과 정답 불일치"
            failed_cases.append((name, reason))

        #7. 결과 출력
        print("패턴: ", name)
        print("Cross 점수: ", score_cross)
        print("X 점수: ", score_x)
        print("판정: ", result)
        print("정답: ", expected)
        print("결과: ", status)
        print("------------")
    
    #8. 최종 결과 요약
    print("=== 결과 요약 ===")
    print("총 테스트: ", total)
    print("통과: ", passed)
    print("실패: ", total - passed)
    
    print("=== 실패 케이스 ===") 

    for name, reason in failed_cases:
        print(name, ":", reason)
           
           
def read_matrix(name):
    matrix = []

    print(name, "입력(3줄)")

    for row in range(3):
        while True:
            text = input(f"{row+1} 행 입력: ")
            values = text.split()
            
            if len(values) != 3:
                print("입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.")
                continue
            try: 
                numbers = []
                for value in values:
                    numbers.append(float(value))

            except ValueError:
                print("숫자만 입력하세요")
                continue
            matrix.append(numbers)
            break
    return matrix


def calculate_mac(pattern, filter_data):
    score = 0.0
    
    for row in range(len(pattern)):
        for col in range(len(pattern[row])):
            score = score + pattern[row][col] * filter_data[row][col]
    
    return score


def decide(score_cross, score_x):
    if abs(score_cross - score_x) < 1e-9:
        return "UNDECIDED"
    elif score_cross > score_x: 
        return "Cross"
    else:
        return "X"
        
def normalize_label(label):
    label = label.strip().lower()
    if label == "+" or label == "cross":
        return "Cross"
    elif label == "x":
        return "X"
    else:
        raise ValueError("알 수 없는 라벨: " + label)

def run_manual_mode():
    filter_a = read_matrix("필터 A")
    filter_b = read_matrix("필터 B")

    print("필터 저장 완료")
    print("A: ", filter_a)
    print("B: ", filter_b)
    pattern = read_matrix("패턴")

    print("패턴 입력 완료!")
    print("MAC 계산을 시작합니다.")   
    
    score_a = calculate_mac(pattern, filter_a)
    score_b = calculate_mac(pattern, filter_b)

    print("Score A:", score_a)
    print("Score B:", score_b)

    if abs(score_a - score_b) < 1e-9:
        print("판정: Undecided")
    elif score_a > score_b:
        print("판정: A")
    else:
        print("판정: B")


print ("=== Mini NPU Simulator ===")

while True:
    print("1. 사용자 입력 (3X3)")
    print("2. data.json 분석")

    choice = input("선택: ")

    if choice == "1":
        run_manual_mode()
        break
    elif choice == "2":
        run_json_mode()
        break
    else:
        print("1 또는 2를 입력하세요")
