

# README.md

Corrections are always welcome
English and Korean ver. are in this docs.
The datasource from AI HUB



# SignLens

## Overview
SignLens is a system that automatically detects objects within images and generates tags using the OpenAI vision model. Users can review and edit the generated tags through a PyQt5-based desktop interface. The system implements a human-in-the-loop feedback loop, aiming to continuously improve the accuracy of robotic vision.

## Key Challenges
Designing a human-in-the-loop labeling system to enhance robotic vision performance
Integrating OpenAI GPT-4o API for real-world object recognition
Developing a PyQt5-based interface that allows users to review and correct tags

## Development Schedule
Project Start: Fri, 2025.10.10
First Mid-Report: Sun, 2025.10.12
First Upload: Tue, 2025.10.14
Final Report / Second Upload: Fri, 2025.10.17

## Background
Modern robotics heavily relies on precise visual recognition. However, datasets often contain incorrect labels or incomplete annotations. This project addresses this issue by combining AI-based auto-tagging with human feedback, improving the quality of training data for robotic vision systems.

## Tech Stack
Language: Python
UI Framework: PyQt5
Database: SQLite
sensetive info: .env
AI Model: OpenAI GPT-4o (Image Recognition API)
Version Control: GitHub

## System Architecture
1. User uploads an image
2. Enter prompt and request description
3. OpenAI vision model automatically generates tags
4. Output results and automatically save to the database
5. Display tags in the PyQt5 GUI
6. User reviews and provides feedback on the tags
7. Corrected feedback is stored in the SQLite database for model improvement

## Key Features
Automated Object Recognition: Automatically detects shopsign ans text within images and generates tags
Editable Tagging Interface: Users can review and modify tags directly Feedback Loop-Based Improvement: Model quality improves continuously using user feedback data
Statistics Dashboard: Visualizes tagging results and accuracy metrics

## Example
(Insert example images and tag tables here)

## Future Improvements
open several images together
Integrate CLIP-based fine-tuning to improve tag accuracy
Enhance auto-tagging performance using accumulated user feedback data
Extend to video-based tagging for continuous frame analysis

## Image Sources
Singboard images are sourced from [AI HUB]
https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=71298

## Developer Info
Developer: [CHANG-HWAN CHEON][https://github.com/chandev123]
Project Scope: SignLens – Automatic Signboard Image Tagging System
Key Challenges: Human-in-the-loop feedback system implementation, tag accuracy optimization
Potential Applications: Robotic vision, outdoor object recognition, automated data labeling tools



# README.md

수정사항은 언제든지 환영합니다
영어와 한글로 문서를 작성했습니다
원본 데이터는 AI HUB에서 가져왔습니다



# 간판렌즈(SignLens)

## 개요
OpenAI 비전 모델을 활용하여 이미지 내 객체를 자동으로 탐지하고, 태그를 생성하는 시스템입니다. 사용자는 PyQt5 기반의 데스크톱 인터페이스에서 태그를 직접 검토, 수정할 수 있습니다. 사용자 피드백 루프(human-in-the-loop)를 구현하여 로봇비전 시스템의 인식 정확도를 지속적으로 개선하는 것을 목표로 합니다.

## 주요 도전과제
로봇비전 성능향상을 위한 사용자 피드백 루프(Human-in-the-loop) 기반 라벨링 시스템 설계
실제 환경객체 인식을 위해 OpenAI GPT-4o API 통합
사용자가 태그 검토, 수정할 수 있는 PyQt5 기반의 인터페이스 개발

## 개발일정
작업시작: 2025.10.10금
1차 중간보고: 2025.10.12일
1차 업로드: 2025.10.14화
최종보고/2차 업로드: 2025.10.17금

## 개발배경
현대 로보틱스는 정밀한 시각인식에 크게 의존합니다. 그러나 잘못된 라벨이 붙거나 불완전한 주석이 포함된 경우가 많습니다. 이 프로젝트는 AI 자동태깅 기능과 사용자의 검증 피드백을 결합하여 로봇비전 학습용 데이터의 품질을 높일 필요성이 있습니다.

## 기술스택
언어: Python
UI 프래임워크: PyQt5
DB: SQLite
민감정보: .env
AI 모델: OpenAI GPT-4o(이미지 인식 API)
버전관리: GitHub

## 시스템 아키텍쳐
1. 사용자가 이미지 업로드
2. 프롬프트 입력, 설명요청
3. OpenAI 비전모델이 태그 자동생성
4. 결과 출력 및 DB 자동저장
5. PyQt5 GUI에 태그표시
6. 사용자가 태그 피드백
7. 수정된 피드백이 SQLite DB에 저장되어 모델 개선에 활용

## 주요기능
자동 객체인식: 이미지 내 간판과 간판 텍스트를 자동탐지 및 태그화
수정가능한 태깅 인터페이스: 사용자가 직접 태그를 검토, 수정가능
피드백 루프기반 개선: 사용자 피드백 데이터를 통해 모델품질 향상
통계 대시보드: 태깅결과 및 정확도 통계 시각화

## 예시

## 향후 개선방향
파일 다중선택 및 예외처리
CLIP 기반 파인튜닝(fine-tuning) 모델연동으로 태그 정확도 향상
누적된 피드백 데이터를 활용한 자동태그 생성 성능 개선
비디오단위 태깅기능 확장(연속 프레임 분석)

## 이미지 출처
간판 이미지의 출처는 AI HUB 입니다.
https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=71298

## 개발자 정보
개발자: [CHANG-HWAN CHEON][https://github.com/chandev123]
프로젝트 성격: 간판 이미지 자동태깅 시스탬(SignLens)
도전과제: 사용자 검증기반 구조(Human-in-the-loop) 구축, 태그 정확도 최적화
활용 가능성: 로봇 비전, 실외 객체 인식, 자동 데이터 라벨링 도구 등