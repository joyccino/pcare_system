# pcare_system

* 환경 : MacOS Catalina, python 3.8
* DB : pymongo atlas

#1 Create and activate a virtual environment: <br>
<img width="453" alt="Screen Shot 2021-10-16 at 12 03 42 PM" src="https://user-images.githubusercontent.com/67300266/137571377-aed3ee82-ef4b-4036-aa25-b0672b385f31.png">

#2 Prepare required libraries from requirements.txt by pip install -r requirements.txt <br>

#3 Run program by 'python3 pcare.py' <br>
![Screen Shot 2021-10-17 at 4 14 12 AM](https://user-images.githubusercontent.com/67300266/137599549-a688b580-d5e4-46f6-a59a-0d7afcf9d5c8.png)

#4 Press keys to navigate:
- Press a or A to insert 'drug.csv' file into current database.<br> <img width="567" alt="Screen Shot 2021-10-17 at 7 16 17 PM" src="https://user-images.githubusercontent.com/67300266/137622896-7c784ff3-9697-404a-a42e-21caeb2307c3.png">

<br> 이때, 입력받는 파일명은 파일형식인 '.csv'를 포함하거나 포함하지 않아도 됩니다.

- Press b or B to insert 'disease.csv' file into current database. <br> <img width="564" alt="Screen Shot 2021-10-17 at 7 18 11 PM" src="https://user-images.githubusercontent.com/67300266/137622899-52e94d50-b237-4f87-ac39-105a448520ec.png">

<br> 이때, 입력받는 파일명은 파일형식인 '.csv'를 포함하거나 포함하지 않아도 됩니다.

- Press c or C to insert 'prescription string' into current database. <br>![Screen Shot 2021-10-17 at 6 25 59 PM](https://user-images.githubusercontent.com/67300266/137621084-0123b2c0-fa55-4e15-a16d-a6b19808cf04.png)
<br> 파싱 작업 추가되었고 사용한 규칙은 아래와 같음: 
<br> 1) 질병명은 생략될 수 있거나 '.' 이 생략될 수 있으며 중간에 의미 없이 빈 문자열을 포함 할 수 있음.
<br> 2) 약 정보는 반드시 1개 이상 입력 되어야 하고 Drug 테이블의 drug_name 과 정확히 일치해야 하며,
<br> 3) '약 이름' 다음 문자열로 '총 투약일수 정보가 '일' 문자열과 붙어서 입력됨.
<br> 4) 처방전 발급 날짜는 생략된 경우 '오늘' 로 입력됨.
- Press d or D for personalised service:
<br> 1) Continue pressing a or A for '나의 질병명과 유용한 정보 알기' <br>![Screen Shot 2021-10-17 at 6 26 15 PM](https://user-images.githubusercontent.com/67300266/137621097-039e6be3-49f6-40a3-a6dd-741cb79566c1.png)

<br> 2) Continue pressing b or B for ' 나의 오늘 복용할 약의 이름과 투약 횟수 알기'<br>![Screen Shot 2021-10-17 at 6 26 24 PM](https://user-images.githubusercontent.com/67300266/137621102-6d84910e-859f-4f2d-9e2b-5c7722db77e4.png)

- Press q or Q to terminate. <br>![Screen Shot 2021-10-17 at 6 29 31 PM](https://user-images.githubusercontent.com/67300266/137621119-e0adfed5-431b-43c1-8ce3-5d3ca82ac753.png)

