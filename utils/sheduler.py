from datetime import datetime
from Algostructured_new import Find_attend


def execute_functions(known_face_encodings, known_face_names):
    # current_time = datetime.now().time()
    current_minute = int(datetime.now().strftime("%H%M"))
    final_list = {}
    i=0
    while i<2:
        print(current_minute)
        if current_minute > 1400 & current_minute <= 1550:
            first_half = Find_attend(known_face_encodings, known_face_names,1)
        elif current_minute > 1550 & current_minute <= 1700:
            second_half = Find_attend(known_face_encodings, known_face_names,2)
        else:
            print("pass")
        i+=1
    for i in second_half:
        if second_half[i] not in first_half:
            pass
        else:
            first_half[i].append(second_half[i])
    return first_half

print(datetime.now().time())