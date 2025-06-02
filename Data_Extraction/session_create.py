import subprocess, argparse, pathlib, getpass, sys, shutil

"""
자동 세션 생성기
- 크롬이나 브라우저에 인스타그램을 켜놓은 상태로 실행
 - 세션 파일이 있으면 아무것도 하지 않음
 - 없으면 ① 브라우저 쿠키(chrome)로 시도
          ② 실패 ➜ 비밀번호로 로그인(프롬프트)
사용 예:
    python session_create.py --user k_siw00
crontab 등에 올려 두면 세션 만료(약 30일) 시 자동 갱신.

required_lib: browser-cookie3 없을시 설치 필요
"""

def run(cmd: list[str]) -> bool:
    """명령 실행 후 성공 여부 반환"""
    proc = subprocess.run(cmd, capture_output = True, text = True)
    if proc.returncode == 0:
        print(proc.stdout.strip())
        return True
    print(proc.stderr.strip())
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", required = True, help = "Instagram ID")
    ap.add_argument("--session", help = "세션 파일 경로", default = None)
    ap.add_argument("--browser", default = "chrome", help = "쿠키를 가져올 브라우저 (chrome, safari, edge, firefox...)")
    args = ap.parse_args()

    # -- 세션 파일 경로 설정
    sess_path = pathlib.Path(args.session or f"{args.user}.session").expanduser()
    if sess_path.exists():
        print("해당 유저의 세션 파일이 이미 존재합니다.", sess_path)
        sys.exit(0)
    
    # -- 브라우저 쿠키로 세션 만들기 (유저 세션 파일이 존재 안할 경우)
    if shutil.which("instaloader") is None:
        sys.exit("instaloader이 path에 존재하지 않습니다. pip install instaloader로 설치 후 다시 진행해주세요.")

    print("세션 없음 -> 브라우저 쿠키 시도")
    ok = run(["instaloader", 
              "--load-cookies", args.browser,
              "--sessionfile", str(sess_path)])
    if ok and sess_path.exists():
        print("브라우저 쿠키로 세션 저장 완료:", sess_path)
        sys.exit(0)

if __name__ == "__main__":
    main()