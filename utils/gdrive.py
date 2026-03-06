# -*- coding: utf-8 -*-
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 파일 생성 및 수정 권한
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_service(base_dir):
    """Google Drive API 서비스 객체 생성 (OAuth 인증)"""
    creds = None
    token_path = os.path.join(base_dir, 'token.json')
    creds_path = os.path.join(base_dir, 'credentials.json')
    
    # 기존 토큰 확인
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
    # 토큰이 없거나 유효하지 않으면 새로 인증
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                raise FileNotFoundError("credentials.json 파일을 찾을 수 없습니다. Google Cloud Console에서 다운로드하여 프로젝트 루트에 넣어주세요.")
            
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
            
        # 새 토큰 저장
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def upload_file(file_path, base_dir):
    """파일을 Google Drive에 업로드 (이미 존재하면 업데이트)"""
    try:
        service = get_service(base_dir)
        filename = os.path.basename(file_path)
        
        # 기존 파일 검색 (삭제되지 않은 파일 중 이름이 같은 것)
        query = f"name = '{filename}' and trashed = false"
        results = service.files().list(q=query, fields="files(id)").execute()
        items = results.get('files', [])
        
        media = MediaFileUpload(file_path, resumable=True)
        
        if items:
            # 파일이 존재하면 업데이트 (첫 번째 검색 결과)
            file_id = items[0]['id']
            updated_file = service.files().update(
                fileId=file_id, media_body=media).execute()
            return file_id, "업데이트 완료"
        else:
            # 파일이 없으면 새로 생성
            file_metadata = {'name': filename}
            file = service.files().create(
                body=file_metadata, media_body=media, fields='id').execute()
            return file.get('id'), "업로드 완료"
            
    except Exception as e:
        return None, str(e)