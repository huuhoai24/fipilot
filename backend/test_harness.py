import argparse
import asyncio
import os
import sys
import json
import wave
import struct
import io
import httpx
import websockets

# Ensure Windows console supports Vietnamese Unicode
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

DEFAULT_HTTP_URL = "http://localhost:8000"
DEFAULT_WS_URL = "ws://localhost:8000/ws"

def generate_dummy_wav(duration=1.0, sample_rate=16000) -> bytes:
    """
    Generates a 16kHz 16-bit mono PCM silent WAV file in memory.
    Useful for testing audio transmission without external files.
    """
    num_samples = int(duration * sample_rate)
    # 16-bit silent samples (all zeros)
    data = struct.pack('<' + 'h' * num_samples, *([0] * num_samples))
    
    wav_io = io.BytesIO()
    with wave.open(wav_io, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(data)
    return wav_io.getvalue()

async def test_cv(base_url: str, cv_file_path: str):
    """
    Test the CV extraction API endpoint.
    """
    url = f"{base_url}/api/cv/extract"
    if not os.path.exists(cv_file_path):
        print(f"[-] Error: CV file not found at: {cv_file_path}")
        return False
        
    print(f"[*] Uploading CV: {cv_file_path} to {url}...")
    async with httpx.AsyncClient(timeout=60.0) as client:
        with open(cv_file_path, "rb") as f:
            files = {"file": (os.path.basename(cv_file_path), f, "application/octet-stream")}
            try:
                response = await client.post(url, files=files)
                if response.status_code == 200:
                    print("[+] CV extraction successful!")
                    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
                    return True
                else:
                    print(f"[-] CV extraction failed with status code {response.status_code}")
                    print(response.text)
                    return False
            except Exception as e:
                import traceback
                print(f"[-] Connection error: {e}")
                traceback.print_exc()
                return False

async def get_sessions(base_url: str):
    """
    Lists all sessions from the backend.
    """
    url = f"{base_url}/api/sessions"
    print(f"[*] Fetching sessions from {url}...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                print("[+] List of sessions retrieved:")
                print(json.dumps(response.json(), indent=2, ensure_ascii=False))
                return True
            else:
                print(f"[-] Failed to fetch sessions. Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"[-] Connection error: {e}")
            return False

async def get_report(base_url: str, session_id: int):
    """
    Retrieves the report for a specific session.
    """
    url = f"{base_url}/api/sessions/{session_id}/report"
    print(f"[*] Fetching report for session {session_id} from {url}...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                print(f"[+] Report for Session {session_id}:")
                print(json.dumps(response.json(), indent=2, ensure_ascii=False))
                return True
            else:
                print(f"[-] Failed to fetch report. Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"[-] Connection error: {e}")
            return False

async def simulate_interview(
    base_url: str,
    ws_base_url: str,
    candidate_name: str,
    role: str,
    level: str,
    template_id: str,
    text_mode: bool = True,
    audio_file_path: str = None,
    responses_list: list = None
):
    """
    Simulates a full interview flow over WebSockets.
    """
    # 1. Create session
    create_url = f"{base_url}/api/sessions"
    session_data = {
        "name": candidate_name,
        "role": role,
        "level": level,
        "language": "vi",
        "template_id": template_id
    }
    
    print(f"[*] Creating session at {create_url}...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(create_url, json=session_data)
            if response.status_code != 200:
                print(f"[-] Failed to create session: {response.text}")
                return False
            session_id = response.json()["session_id"]
            print(f"[+] Session created successfully. ID: {session_id}")
        except Exception as e:
            print(f"[-] Error creating session: {e}")
            return False

    # 2. Establish WebSocket connection
    ws_url = f"{ws_base_url}/interview/{session_id}"
    print(f"[*] Connecting to WebSocket: {ws_url}")
    
    if responses_list is None:
        responses_list = [
            "Chào bạn, tôi là một ứng viên sẵn sàng tham gia phỏng vấn vị trí Software Engineer.",
            "Lập trình hướng đối tượng có 4 đặc tính chính là đóng gói, kế thừa, đa hình và trừu tượng.",
            "Tính đóng gói giúp bảo mật trạng thái bên trong đối tượng bằng cách giới hạn quyền truy cập trực tiếp.",
            "Tính kế thừa cho phép các lớp con tái sử dụng các phương thức và thuộc tính của lớp cha.",
            "Tính đa hình cho phép các đối tượng khác nhau thực thi cùng một phương thức theo các cách khác nhau.",
            "Tính trừu tượng giúp ẩn đi các chi tiết triển khai phức tạp và chỉ hiển thị giao diện cần thiết.",
            "Tôi dùng Git để quản lý mã nguồn và thực hiện branching, merging hàng ngày.",
            "Tối ưu truy vấn SQL bằng cách tạo chỉ mục thích hợp và hạn chế quét toàn bảng.",
            "REST API là kiến trúc thiết kế dịch vụ web sử dụng các giao thức HTTP chuẩn.",
            "Tôi thiết kế DB bằng cách chuẩn hóa dữ liệu về dạng chuẩn 3NF để tránh trùng lặp.",
            "Tôi mong muốn đóng góp kỹ năng lập trình và học hỏi thêm về điện toán đám mây."
        ]

    response_index = 0
    audio_bytes_payload = None
    
    if not text_mode:
        if audio_file_path and os.path.exists(audio_file_path):
            print(f"[*] Loaded custom audio file: {audio_file_path}")
            with open(audio_file_path, "rb") as f:
                audio_bytes_payload = f.read()
        else:
            print("[*] No custom audio file provided or file not found. Generating dummy silent WAV file...")
            audio_bytes_payload = generate_dummy_wav(duration=1.5)

    try:
        async with websockets.connect(ws_url) as ws:
            print("[+] WebSocket connection established.")
            audio_counter = 0
            
            while True:
                try:
                    message = await ws.recv()
                    
                    if isinstance(message, str):
                        # Text JSON message
                        data = json.loads(message)
                        sender = data.get("sender", "AI")
                        text = data.get("text", "")
                        status = data.get("status", "RUNNING")
                        
                        print(f"\n[{sender}]: {text}")
                        print(f"[Status]: {status}")
                        
                        if status == "ENDED":
                            print("\n[+] Interview session ended by server.")
                            break
                            
                        # If AI spoke, prepare next answer
                        if sender == "AI" or sender == "Alex":
                            if response_index < len(responses_list):
                                user_ans = responses_list[response_index]
                                response_index += 1
                                await asyncio.sleep(1.5) # Simulate natural pause
                                
                                if text_mode:
                                    print(f"[- Sending Text]: {user_ans}")
                                    # Send JSON containing text response
                                    await ws.send(json.dumps({"text": user_ans}))
                                else:
                                    print(f"[- Sending Audio Bytes] (Simulating: {user_ans})")
                                    await ws.send(audio_bytes_payload)
                            else:
                                print("[*] Run out of mock responses. Waiting for server to close or timeout.")
                                await asyncio.sleep(5)
                                break
                                
                    else:
                        # Binary audio output from server (TTS)
                        audio_counter += 1
                        out_filename = f"tts_output_session_{session_id}_{audio_counter}.wav"
                        # We can save it for debugging purposes
                        with open(out_filename, "wb") as f:
                            f.write(message)
                        print(f"  [Binary TTS Audio Received: {len(message)} bytes, saved to {out_filename}]")
                        
                except websockets.exceptions.ConnectionClosed as ecc:
                    print(f"\n[-] WebSocket connection closed by server: {ecc}")
                    break
                    
    except Exception as e:
        print(f"[-] WebSocket error: {e}")
        return False

    # 3. Retrieve final report
    print("\n[*] Waiting 2 seconds for final report generation...")
    await asyncio.sleep(2)
    await get_report(base_url, session_id)
    return True

async def simulate_early_stop(base_url: str, ws_base_url: str, template_id: str):
    """
    Simulates early stopping by giving 3 consecutive Wrong answers.
    """
    print("\n" + "="*50)
    print("[*] Starting Early Stopping Test Case...")
    print("="*50)
    
    # Answers that will score poorly and satisfy prompt non-answers
    non_answers = [
        "tôi chịu, không biết",
        "bỏ qua câu này đi",
        "tôi không muốn trả lời câu này, tiếp tục đi"
    ]
    
    # We will simulate text mode since it is deterministic for evaluation testing
    success = await simulate_interview(
        base_url=base_url,
        ws_base_url=ws_base_url,
        candidate_name="Nguyen Van Fail",
        role="Software Engineer",
        level="Junior",
        template_id=template_id,
        text_mode=True,
        responses_list=non_answers
    )
    
    if success:
        print("[+] Early stopping test executed. Review the output report score/feedback above.")
    else:
        print("[-] Early stopping test failed to execute.")

def main():
    parser = argparse.ArgumentParser(description="AI Interview Platform Test & Simulation Harness")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # test-cv
    cv_parser = subparsers.add_parser("test-cv", help="Test CV Parsing API")
    cv_parser.add_argument("--file", default="mock_cv.docx", help="Path to CV file")
    cv_parser.add_argument("--url", default=DEFAULT_HTTP_URL, help="Base HTTP URL of backend")
    
    # test-sessions
    subparsers.add_parser("test-sessions", help="List all interview sessions")
    
    # test-report
    report_parser = subparsers.add_parser("test-report", help="Fetch a session report")
    report_parser.add_argument("session_id", type=int, help="Session ID to fetch")
    report_parser.add_argument("--url", default=DEFAULT_HTTP_URL, help="Base HTTP URL of backend")
    
    # test-interview
    interview_parser = subparsers.add_parser("test-interview", help="Simulate a full interview session")
    interview_parser.add_argument("--name", default="Candidate Test", help="Candidate Name")
    interview_parser.add_argument("--role", default="Software Engineer", help="Role target")
    interview_parser.add_argument("--level", default="Junior", help="Inferred level (Junior, Mid, Senior)")
    interview_parser.add_argument("--template", default="Software_Engineer_lv1.md", help="Template file name")
    interview_parser.add_argument("--audio", action="store_true", help="Run in audio simulation mode (instead of text)")
    interview_parser.add_argument("--audio-file", default=None, help="Optional WAV/MP3 file to transmit in audio mode")
    interview_parser.add_argument("--url", default=DEFAULT_HTTP_URL, help="Base HTTP URL of backend")
    interview_parser.add_argument("--ws-url", default=DEFAULT_WS_URL, help="Base WS URL of backend")
    
    # test-early-stop
    early_stop_parser = subparsers.add_parser("test-early-stop", help="Validate early stopping functionality")
    early_stop_parser.add_argument("--template", default="Software_Engineer_lv1.md", help="Template file name")
    early_stop_parser.add_argument("--url", default=DEFAULT_HTTP_URL, help="Base HTTP URL of backend")
    early_stop_parser.add_argument("--ws-url", default=DEFAULT_WS_URL, help="Base WS URL of backend")

    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
        
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        if args.command == "test-cv":
            loop.run_until_complete(test_cv(args.url, args.file))
        elif args.command == "test-sessions":
            loop.run_until_complete(get_sessions(DEFAULT_HTTP_URL))
        elif args.command == "test-report":
            loop.run_until_complete(get_report(args.url, args.session_id))
        elif args.command == "test-interview":
            loop.run_until_complete(simulate_interview(
                base_url=args.url,
                ws_base_url=args.ws_url,
                candidate_name=args.name,
                role=args.role,
                level=args.level,
                template_id=args.template,
                text_mode=not args.audio,
                audio_file_path=args.audio_file
            ))
        elif args.command == "test-early-stop":
            loop.run_until_complete(simulate_early_stop(
                base_url=args.url,
                ws_base_url=args.ws_url,
                template_id=args.template
            ))
    except KeyboardInterrupt:
        print("\n[-] Testing interrupted by user.")
    finally:
        loop.close()

if __name__ == "__main__":
    main()
