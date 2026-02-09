# -*- coding: utf-8 -*-
"""
AI 분석 모듈 (Gemini API)
- 로또 번호 패턴 분석 및 질의응답 처리
"""
import os
from google import genai
from google.genai import types

def analyze_lotto_patterns(history_text, user_question, api_key):
    """
    Gemini API를 사용하여 로또 번호 패턴을 분석하고 사용자 질문에 답변합니다.
    
    Args:
        history_text (str): 분석할 로또 당첨번호 이력 텍스트
        user_question (str): 사용자 질문
        api_key (str): Google Gemini API Key
        
    Returns:
        str: AI 답변 텍스트
        
    Raises:
        Exception: API 호출 실패 시 예외 발생
    """
    if not api_key:
        raise ValueError("API 키가 설정되지 않았습니다.")

    prompt = f"""
당신은 로또 번호 분석 전문가입니다. 다음 데이터를 바탕으로 사용자의 질문에 답변해주세요.
{history_text}

사용자 질문: {user_question}

답변은 친절하고 전문적으로, 그리고 확률적 근거(홀짝, 번호대, 미출현 번호 등)를 들어 설명해주세요.
답변 끝에는 "이 분석은 참고용이며, 당첨을 보장하지 않습니다."라는 문구를 추가해주세요.
"""

    client = genai.Client(api_key=api_key)
    
    # 모델 호출 (2.0-flash -> 2.0-flash-lite fallback)
    # 2.0-flash가 가장 빠르고 성능이 좋음
    primary_model = 'gemini-2.0-flash'
    fallback_models = ['gemini-2.0-flash-lite', 'gemini-1.5-flash']
    
    try:
        response = client.models.generate_content(
            model=primary_model,
            contents=prompt
        )
        return response.text
    except Exception as e:
        error_msg = str(e)
        # 429 Quota Exceeded 또는 기타 에러 발생 시 fallback 시도
        if '429' in error_msg or 'RESOURCE_EXHAUSTED' in error_msg or 'NOT_FOUND' in error_msg:
            print(f'[Gemini API] {primary_model} failed ({error_msg[:50]}...). Trying fallbacks...')
            
            for model_name in fallback_models:
                try:
                    print(f'[Gemini API] Trying {model_name}...')
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                    return response.text
                except Exception as e2:
                    print(f'[Gemini API] {model_name} failed.')
                    continue
            
            # 모든 fallback 실패 시
            raise Exception("All Gemini models failed.")
        else:
            raise e
