Translate-Word
=============
다수의 영단어를 Daum 사전에서 크롤링해 비동기적으로 가져옵니다.
* Daum 사전: https://dic.daum.net/index.do

시작
=============
전제 조건
-------------
```
requests >= 2.26.0
beautifulsoap4 >= 4.9.1
```

사용 예시
-------------

* 터미널에서 python main.py로 실행합니다.
* 키워드를 입력합니다.

예제
-------------
```
C:\> python main.py
=====================================================        
키워드를 입력해주세요
(* abc순 정렬이 권장되고, 키워드는 스페이스로 구분됩니다.) >>
apple banana kiwi blueberry strawberry 
=====================================================
blueberry 성공, 20.000% 진행 (1/5)
banana 성공, 40.000% 진행 (2/5)
apple 성공, 60.000% 진행 (3/5)
kiwi 성공, 80.000% 진행 (4/5)
strawberry 성공, 100.000% 진행 (5/5)
=====================================================
잠시만 기다려주세요..
결과를 줄바꿈하실건가요? (기본값 y, y/n) >>>
애플, 사과, 사과나무, 뉴욕 
바나나
블루베리, 그 관목, 월귤나무
키위, 뉴질랜드인, 무익조   
딸기
=====================================================
[성공: 5, 실패: 0, 미반환: 0], 총계: 5
28.7352초 소요됨
```