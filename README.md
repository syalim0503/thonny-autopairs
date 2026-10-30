# Thonny 괄호·따옴표 자동완성 플러그인

Thonny 5용 자동완성 플러그인입니다. 설치 방법은 운영체제에 따라 다릅니다.

## 기능

- 괄호 `( [ {`와 따옴표 `" '`를 자동으로 닫습니다.
- 닫는 문자를 입력하면 건너뜁니다.
- 빈 쌍에서 Backspace를 누르면 쌍을 함께 지웁니다.
- 괄호 안에서 Enter를 누르면 닫는 괄호가 다음 줄로 내려갑니다.
- 글자를 선택한 뒤 괄호나 따옴표를 입력하면 선택 영역을 감쌉니다.
- `"""`를 세 번 입력하면 `"""|"""` 형태로 닫습니다.
- Tools > Options > Auto-pairs에서 켜고 끌 수 있습니다.

## 저장소 구성

| 폴더 | 대상 | 설치 파일 |
| --- | --- | --- |
| `thonny-autopairs-windows/` | Windows | `install_helper.py` (Thonny에서 실행) |
| `thonny-plugins/` | macOS | `install.command` |

두 폴더의 `thonnycontrib/autopairs.py`는 같은 파일입니다.

## Windows 설치

1. `thonny-autopairs-windows/` 폴더를 받아 압축을 풉니다.
2. `install_helper.py`를 Thonny에서 엽니다. Run(F5)을 누르면 Thonny의 Python이 실행되어 플러그인을 복사합니다.
3. Thonny를 껐다가 다시 엽니다.

실행이 안 되거나 `thonny` 모듈을 찾지 못하면 수동 설치를 사용하세요.

## macOS 설치

1. `thonny-plugins/` 폴더에서 `install.command`를 더블클릭합니다. 막히면 우클릭 > 열기를 사용하거나 터미널에서 `bash install.command`를 실행합니다.
2. Thonny를 재시작합니다.

## 수동 설치

- Windows: Thonny에서 Tools > Open Thonny data folder...를 연 뒤 `plugins\Python3XX\site-packages\thonnycontrib\` 폴더에 `autopairs.py`를 복사합니다. `Python3XX`는 Thonny에 포함된 Python 버전입니다(예: `Python313`).
- macOS: `~/Library/Thonny/plugins/lib/python/site-packages/thonnycontrib/` 폴더에 `autopairs.py`를 복사합니다.

## 삭제

설치된 `thonnycontrib` 폴더에서 `autopairs.py`를 지운 뒤 Thonny를 재시작합니다.

## 라이선스

MIT License. 자세한 내용은 [LICENSE](LICENSE)를 참고하세요.
