"""
초기 샘플 데이터를 데이터베이스에 추가하는 스크립트
"""
from datetime import datetime, timedelta
from database import SessionLocal
from models import User, Activity, Subscription

def init_sample_data():
    db = SessionLocal()
    
    try:
        # 기존 활동 데이터 확인 및 삭제
        existing_activities = db.query(Activity).count()
        if existing_activities > 0:
            print(f"기존 활동 {existing_activities}개를 삭제하고 새로 추가합니다.")
            db.query(Activity).delete()
            db.commit()
        
        # 샘플 사용자 생성 (기존 사용자가 없을 때만)
        existing_users = db.query(User).count()
        user1 = None
        if existing_users == 0:
            user1 = User(
                name="홍길동",
                email="hong@example.com",
                phone="010-1234-5678",
                age=65,
                address="서울시 강남구"
            )
            user2 = User(
                name="김영희",
                email="kim@example.com",
                phone="010-2345-6789",
                age=72,
                address="서울시 서초구"
            )
            db.add(user1)
            db.add(user2)
            db.commit()
            db.refresh(user1)
            db.refresh(user2)
            
            # 구독 생성
            subscription1 = Subscription(
                user_id=user1.id,
                plan_type="monthly",
                start_date=datetime.utcnow(),
                end_date=datetime.utcnow() + timedelta(days=30),
                is_active=True
            )
            db.add(subscription1)
            db.commit()
        else:
            # 기존 사용자 중 첫 번째 사용자 가져오기
            user1 = db.query(User).first()
        
        # 샘플 활동 생성
        activities = [
            Activity(
                title="도예 클래스 - 손으로 만드는 나만의 그릇",
                description="""직접 흙을 빚어 나만의 그릇을 만들어보는 시간입니다. 
초보자도 쉽게 따라할 수 있도록 친절하게 안내해드립니다. 
도예의 기본 기법부터 장식 방법까지 배울 수 있으며, 완성된 작품은 가마에서 구워서 
2주 후에 수령하실 수 있습니다. 손의 정밀한 움직임을 통해 집중력 향상과 스트레스 해소에도 도움이 됩니다.
모든 재료와 도구는 제공되며, 복장은 편안한 옷을 입어주시면 됩니다.""",
                category="도예/공예",
                location="서울시 강남구 테헤란로 123 도예공방",
                instructor="이도예 (도예작가, 15년 경력)",
                max_participants=10,
                duration_minutes=120,
                price=50000,
                image_url="https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop",
                activity_date=datetime.utcnow() + timedelta(days=7)
            ),
            Activity(
                title="실버 수영 교실",
                description="""시니어 분들을 위한 안전하고 즐거운 수영 수업입니다. 
개인 체력에 맞춘 맞춤형 프로그램을 제공하며, 관절에 부담을 주지 않는 부드러운 수영 자세를 
배울 수 있습니다. 수영은 전신 운동으로 심폐 기능 향상과 근력 강화에 탁월하며, 
정기적으로 참여하시면 건강 관리에 큰 도움이 됩니다. 
보조 도구와 튜브를 사용하여 안전하게 진행되며, 초보자도 부담 없이 시작할 수 있습니다.
체육관 내 샤워실과 탈의실, 락커가 완비되어 있습니다.""",
                category="수영",
                location="서울시 서초구 서초대로 456 실버 수영장",
                instructor="박수영 (수영 지도사, 시니어 전담)",
                max_participants=15,
                duration_minutes=60,
                price=30000,
                image_url="https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=800&h=600&fit=crop",
                activity_date=datetime.utcnow() + timedelta(days=10)
            ),
            Activity(
                title="원두 커피 시음 체험",
                description="""다양한 원두를 시음하며 커피의 맛과 향을 이해하는 시간입니다. 
에티오피아, 콜롬비아, 브라질 등 세계 각국의 프리미엄 원두를 직접 맛보실 수 있으며,
각 원두의 특성과 로스팅 정도에 따른 맛의 차이를 배울 수 있습니다. 
간단한 드립 방법(핸드드립, 프렌치프레스 등)도 배워서 집에서도 활용할 수 있습니다.
커피 전문가가 함께하시며, 커피와 어울리는 디저트도 함께 제공됩니다.
커피에 대해 처음 접하시는 분도 환영합니다.""",
                category="커피 시음",
                location="서울시 강남구 논현로 789 로스팅 카페",
                instructor="최커피 (Q-Grader, 커피 전문가)",
                max_participants=12,
                duration_minutes=90,
                price=25000,
                image_url="https://images.unsplash.com/photo-1517487881594-2787fef5ebf7?w=800&h=600&fit=crop",
                activity_date=datetime.utcnow() + timedelta(days=14)
            ),
            Activity(
                title="요가 클래스 - 치유와 평안",
                description="""부드러운 동작으로 몸과 마음을 편안하게 만드는 요가 수업입니다. 
의자에 앉아서도 할 수 있는 동작들을 중심으로 진행하며, 서 있을 때와 누워있을 때의 
동작도 포함되어 있습니다. 호흡법을 배워 스트레스 관리와 집중력 향상에 도움이 되며,
근육의 유연성 향상과 관절 건강에 좋습니다. 
매트와 블록, 벨트 등 필요한 용품은 모두 제공되며, 편안한 복장으로 참여해주시면 됩니다.
수업 후에는 명상 시간도 가져 몸과 마음의 평안을 찾을 수 있습니다.""",
                category="요가/필라테스",
                location="서울시 서초구 잠원로 321 요가 스튜디오",
                instructor="정요가 (요가 지도사, 시니어 전문)",
                max_participants=20,
                duration_minutes=75,
                price=20000,
                image_url="https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&h=600&fit=crop",
                activity_date=datetime.utcnow() + timedelta(days=5)
            ),
            Activity(
                title="한식 요리 클래스 - 건강한 밥상",
                description="""건강하고 맛있는 한식을 직접 만들어보는 요리 클래스입니다. 
시니어 분들도 쉽게 만들 수 있는 레시피를 제공하며, 영양 균형을 고려한 메뉴로 구성됩니다.
이번 수업에서는 된장찌개, 두부조림, 시금치나물 등 집에서 자주 먹는 반찬들을 만들어봅니다.
모든 재료는 신선한 것을 준비해드리며, 요리 후에는 함께 식사를 하며 대화를 나눌 수 있습니다.
레시피 카드를 제공해 집에서도 쉽게 따라 만들 수 있습니다. 
앞치마와 요리 도구는 모두 제공되니 손만 깨끗하게 씻고 오시면 됩니다.""",
                category="요리 클래스",
                location="서울시 강남구 도산대로 654 요리 교실",
                instructor="한요리 (한식 전문 요리사)",
                max_participants=8,
                duration_minutes=150,
                price=45000,
                image_url="https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&h=600&fit=crop",
                activity_date=datetime.utcnow() + timedelta(days=12)
            ),
            Activity(
                title="원예 클래스 - 나만의 정원 가꾸기",
                description="""화분에 나만의 식물을 심고 가꾸는 방법을 배우는 원예 클래스입니다.
다육식물, 허브, 꽃 등 다양한 식물 중 원하는 것을 선택하여 심을 수 있으며,
물주기, 거름주기, 햇빛 관리 등 식물을 건강하게 키우는 노하우를 배울 수 있습니다.
완성된 화분은 집으로 가져가실 수 있으며, 식물을 키우는 과정에서 
스트레스 해소와 성취감을 느낄 수 있습니다. 
식물 선택에 대한 전문가 상담도 제공되며, 초보자도 쉽게 시작할 수 있습니다.
화분, 흙, 식물, 도구 등 모든 재료가 포함되어 있습니다.""",
                category="원예",
                location="서울시 강남구 선릉로 987 원예 센터",
                instructor="김원예 (원예 전문가, 조경기사)",
                max_participants=15,
                duration_minutes=90,
                price=35000,
                image_url="https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800&h=600&fit=crop",
                activity_date=datetime.utcnow() + timedelta(days=9)
            ),
            Activity(
                title="우쿨렐레 클래스 - 즐거운 연주",
                description="""시니어 분들을 위한 우쿨렐레 기초 클래스입니다.
우쿨렐레는 작고 가볍고 배우기 쉬워 시니어에게 최적의 악기입니다.
기본 코드와 스트로크부터 시작하여 간단한 곡을 연주할 수 있도록 지도합니다.
우쿨렐레를 직접 연주하며 즐거움과 성취감을 느낄 수 있고, 
음악을 통해 뇌 건강에도 좋은 영향을 줍니다.
악기는 대여해드리며, 수업이 끝난 후에도 연습할 수 있도록 
연습용 악기를 개인적으로 구매하실 수 있습니다.
음악을 처음 접하시는 분도 환영하며, 친구들과 함께 합주할 수 있는 시간도 있습니다.""",
                category="음악/악기",
                location="서울시 서초구 반포대로 147 음악 교실",
                instructor="강음악 (우쿨렐레 지도사)",
                max_participants=12,
                duration_minutes=90,
                price=30000,
                image_url="https://images.unsplash.com/photo-1511735111819-9a3f7709049c?w=800&h=600&fit=crop",
                activity_date=datetime.utcnow() + timedelta(days=11)
            ),
            Activity(
                title="독서 모임 - 인문학 이야기",
                description="""좋은 책을 함께 읽고 생각을 나누는 독서 모임입니다.
매 달 선정된 책을 읽고 모여서 토론하며, 다양한 관점에서 이야기를 나눕니다.
이번 달의 도서는 '노년을 위한 철학'이며, 인생의 지혜와 삶의 의미에 대해 
함께 생각해볼 수 있는 시간입니다. 
책을 읽고 느낀 점, 공감한 부분, 생각해볼 점 등을 자유롭게 이야기하며,
서로의 경험을 공유할 수 있습니다. 독서를 통해 지적 호기심을 충족시키고,
새로운 관점을 발견할 수 있습니다. 
책은 미리 읽어오시거나, 모임에서 간단히 요약 설명도 해드립니다.
편안한 분위기에서 차를 마시며 대화를 나누는 시간입니다.""",
                category="독서 모임",
                location="서울시 강남구 압구정로 258 독서 카페",
                instructor="문독서 (문학평론가, 독서 지도사)",
                max_participants=20,
                duration_minutes=120,
                price=15000,
                image_url="https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800&h=600&fit=crop",
                activity_date=datetime.utcnow() + timedelta(days=15)
            ),
            Activity(
                title="전통 공예 - 한지 공예",
                description="""우리 전통 한지를 이용한 공예를 배워보는 시간입니다.
한지로 만든 소품(연필꽂이, 부채, 장식품 등)을 만들며 전통문화를 체험할 수 있습니다.
한지 공예는 손의 섬세한 움직임이 필요하여 집중력 향상과 인내심을 기를 수 있으며,
예쁜 작품을 완성했을 때의 성취감이 큽니다.
한지의 특성과 활용법을 배우며, 다양한 기법을 실습해볼 수 있습니다.
완성된 작품은 집에 가져가서 사용하실 수 있습니다.
모든 재료와 도구가 제공되며, 초보자도 쉽게 따라할 수 있도록 친절하게 안내합니다.""",
                category="도예/공예",
                location="서울시 서초구 강남대로 369 전통공예관",
                instructor="전통공예 (한지 공예 전문가)",
                max_participants=10,
                duration_minutes=120,
                price=40000,
                image_url="https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=800&h=600&fit=crop",
                activity_date=datetime.utcnow() + timedelta(days=13)
            ),
            Activity(
                title="필라테스 클래스 - 근력과 균형",
                description="""시니어 분들을 위한 맞춤형 필라테스 수업입니다.
근력 강화와 균형 감각 향상에 초점을 맞춘 운동으로, 
일상생활에서 필요한 힘과 안정성을 기를 수 있습니다.
의자에 앉아서 하는 동작과 서서 하는 동작, 바닥에 누워서 하는 동작으로 구성되어 있어
체력에 따라 선택적으로 참여할 수 있습니다.
필라테스는 관절에 부담을 주지 않으면서도 전신 근력을 강화할 수 있어
시니어에게 매우 적합한 운동입니다.
정기적으로 참여하시면 자세 개선과 근골격계 건강에 도움이 됩니다.
매트와 도구는 모두 제공되며, 편안한 운동복을 입어주시면 됩니다.""",
                category="요가/필라테스",
                location="서울시 강남구 테헤란로 753 필라테스 스튜디오",
                instructor="박필라테스 (필라테스 지도사, 물리치료사)",
                max_participants=15,
                duration_minutes=60,
                price=25000,
                image_url="https://images.unsplash.com/photo-1599901860904-17e6ed7083a0?w=800&h=600&fit=crop",
                activity_date=datetime.utcnow() + timedelta(days=8)
            ),
            Activity(
                title="디저트 만들기 - 수제 쿠키와 마카롱",
                description="""예쁘고 맛있는 디저트를 직접 만들어보는 클래스입니다.
수제 쿠키와 마카롱을 만들며 베이킹의 기본을 배울 수 있습니다.
각 단계별로 친절하게 설명해드리며, 초보자도 쉽게 따라할 수 있습니다.
만든 디저트는 예쁜 포장지에 포장하여 집으로 가져가실 수 있으며,
가족들과 함께 나눠 드실 수 있습니다.
레시피 카드를 제공해 집에서도 다시 만들어볼 수 있습니다.
베이킹은 창의적인 활동으로 스트레스 해소와 즐거움을 제공합니다.
앞치마와 모든 재료, 도구가 제공되며, 오븐 사용법도 안전하게 배울 수 있습니다.""",
                category="요리 클래스",
                location="서울시 서초구 서초대로 852 베이킹 스튜디오",
                instructor="디저트 (파티시에, 베이킹 전문가)",
                max_participants=10,
                duration_minutes=120,
                price=45000,
                image_url="https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=800&h=600&fit=crop",
                activity_date=datetime.utcnow() + timedelta(days=16)
            ),
        ]
        
        for activity in activities:
            db.add(activity)
        
        db.commit()
        
        print("✅ 샘플 데이터가 성공적으로 추가되었습니다!")
        print(f"   - 사용자: {db.query(User).count()}명")
        print(f"   - 활동: {db.query(Activity).count()}개")
        print(f"   - 구독: {db.query(Subscription).count()}개")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # 데이터베이스 테이블 생성
    from database import Base, engine
    Base.metadata.create_all(bind=engine)
    
    init_sample_data()

