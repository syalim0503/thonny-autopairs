Thonny 괄호/따옴표 자동완성 플러그인 (Windows, Thonny 5)

기능
- 괄호 ( [ { 와 따옴표 " ' 자동 닫기, 닫는 문자 건너뛰기, 빈 쌍 Backspace로 같이 지우기
- 괄호 안에서 Enter 치면 닫는 괄호를 다음 줄로
- 선택한 글자를 괄호/따옴표로 감싸기, """ 세 개 입력 시 """|"""
- 끄고 켜기: Tools > Options > Auto-pairs

설치
1. 압축을 풀고 install_helper.py 를 Thonny에서 엽니다.
2. Thonny 메뉴의 Run(F5)을 누릅니다. "설치 완료" 메시지가 나오면 성공입니다.
3. Thonny를 껐다가 다시 열기

수동 설치
  1. Thonny에서 Tools > Open Thonny data folder... 를 누르면 Thonny 폴더가 열립니다.
  2. 그 안의 plugins\Python3XX\site-packages\thonnycontrib\ 에 autopairs.py 를 복사
     (폴더가 없으면 만들기. Python3XX는 Thonny에 들어 있는 Python 버전, 예: Python313)

삭제
  위 thonnycontrib 폴더에서 autopairs.py 를 지우고 Thonny 재시작
