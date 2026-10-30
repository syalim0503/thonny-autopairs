Thonny 편의기능 플러그인 (Thonny 5, macOS)

기능
- 괄호 ( [ { 와 따옴표 " ' 자동 닫기, 닫는 문자 건너뛰기, 빈 쌍 Backspace로 같이 지우기
- 괄호 안에서 Enter 치면 닫는 괄호를 다음 줄로
- 선택한 글자를 괄호/따옴표로 감싸기, """ 세 개 입력 시 """|"""
- 끄고 켜기: Tools > Options > Auto-pairs

설치
1. install.command 를 더블클릭 (막히면: 우클릭 > 열기, 또는 터미널에서 bash install.command)
2. Thonny 재시작

수동 설치
  thonnycontrib 폴더 안의 autopairs.py 를 아래 폴더에 복사 (폴더가 없으면 만들기)
  ~/Library/Thonny/plugins/lib/python/site-packages/thonnycontrib/

삭제
  위 폴더에서 autopairs.py 를 지우고 Thonny 재시작
