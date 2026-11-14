# MINGO 작업대 디자인·콘텐츠 계약

- 대상: 기존 공개 GitHub Pages 설치 안내를 프로젝트 문서 허브로 전환한다. 소스/주소는 mingo-mobile-guide를 유지하며 앱/API/관리자 코드를 변경하지 않는다.
- 방향: MINGO white/black museum. 배경 #ffffff, 보조 #f6f6f6, 본문 #202020, 보조 #5b5b5b, 경계 #dddddd. 기존 Pretendard 계열/시스템 한글 폰트 유지. 신규 폰트·추적기·원격 JS 의존성 금지. 그라데이션·웜베이지·장식 KPI·과도한 그림자 금지.
- 실제 문서: 모바일 설치 안내, ART PASS 블록체인 조합 검토 보고서. 추가 문서 작성 방법은 README로 연결. 비어 있는 메뉴·준비중 카드·검색 흉내 금지.
- 루트 index.html은 MINGO 작업대. 기존 설치 안내는 mobile.html로 이동하여 기존 APK/QR/자산 링크를 그대로 보존하고 작업대 복귀 링크 제공. APK 재빌드/업데이트 작업 아님.
- reports/blockchain.html은 한국어 읽기용 보고서, reports/mingo-art-pass-blockchain.md는 다운로드/소스용 전체 보고서. 제목·권고안·한계·조사일·문서정리일·출처가 서로 일치해야 한다. 기술선정 제안과 실제 구현/감사/배포를 구분한다.
- 공개 경계: 이 저장소와 Pages는 공개다. 실제 계정·키·접근 토큰·Atlas/R2 식별자/접속 문자열·사용자 개인정보·로컬 절대경로·내부 작업 로그 금지. 원문 연구 노트 전체를 복사하지 않는다.
- 레이아웃: max-width 약1120px; 문서 본문 약760px; desktop에서 읽기 쉬운 상단 내비/문서 목록, mobile에서 한 열. 한글 본문16px 이상, 보조14px 이상, 링크/버튼 터치영역44px, 명확한 focus-visible, skip link, semantic header/nav/main/footer. 긴 출처 URL·code 줄바꿈/코드 스크롤을 안전하게 처리한다.
- 동작: 기본 HTML/CSS로 모든 콘텐츠와 링크 접근. JS 필수 없음. 상대경로로 /mingo-mobile-guide/ 하위 호스팅을 지원한다. 문서의 출처/목차/Markdown 링크·복귀 링크는 실재해야 한다. 과한 모션 없이 reduced-motion 대응.
- 검증: 로컬 정적 서버의1440/768/375px 렌더·가로넘침·모든 내부 링크/앵커/자산 검사; 실제 Pages SHA/build 완료 및 HTTP·화면 검증. 성능/접근성 공식 인증이나 field vitals 통과로 확대하지 않는다.
