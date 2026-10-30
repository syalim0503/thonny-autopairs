#!/bin/bash
# Thonny 플러그인 설치: 괄호/따옴표 자동완성(autopairs)
# Finder에서 더블클릭하거나, 터미널에서 `bash install.command`로 실행하세요.

cd "$(dirname "$0")" || exit 1

# Thonny.app 찾기
THONNY_APP=""
for candidate in "/Applications/Thonny.app" "$HOME/Applications/Thonny.app"; do
    if [ -d "$candidate" ]; then
        THONNY_APP="$candidate"
        break
    fi
done
if [ -z "$THONNY_APP" ]; then
    THONNY_APP="$(mdfind "kMDItemCFBundleIdentifier == 'org.thonny.Thonny'" 2>/dev/null | head -n 1)"
fi

# Thonny가 쓰는 플러그인 폴더를 Thonny 자신에게 물어보기
DEST=""
THONNY_PY="$THONNY_APP/Contents/Frameworks/Python.framework/Versions/Current/bin/python3"
if [ -n "$THONNY_APP" ] && [ -x "$THONNY_PY" ]; then
    DEST="$("$THONNY_PY" -I -c 'import thonny; print(thonny.get_sys_path_directory_containg_plugins())' 2>/dev/null)"
fi
if [ -z "$DEST" ]; then
    DEST="$HOME/Library/Thonny/plugins/lib/python/site-packages"
    echo "Thonny.app을 찾지 못해 기본 위치에 설치합니다."
fi

mkdir -p "$DEST/thonnycontrib" || exit 1
cp thonnycontrib/autopairs.py "$DEST/thonnycontrib/" || exit 1

echo ""
echo "설치 완료: $DEST/thonnycontrib"
if pgrep -f "Thonny.app/Contents/Resources/thonnymain.py" > /dev/null; then
    echo "Thonny가 실행 중입니다. 종료(Cmd+Q) 후 다시 열면 적용됩니다."
else
    echo "Thonny를 열면 바로 적용됩니다."
fi
