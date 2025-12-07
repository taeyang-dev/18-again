import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api/client'
import './Home.css'

function Home() {
  const [activities, setActivities] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [activitiesRes, categoriesRes] = await Promise.all([
        api.getActivities(),
        api.getCategories()
      ])
      setActivities(activitiesRes.data.slice(0, 6)) // 최근 6개만
      setCategories(categoriesRes.data.categories)
      setLoading(false)
    } catch (error) {
      console.error('데이터 로딩 실패:', error)
      setLoading(false)
    }
  }

  return (
    <div className="home">
      <section className="hero">
        <h1>시니어를 위한 특별한 체험</h1>
        <p>도예, 수영, 커피 시음 등 다양한 활동을 구독형으로 즐기세요</p>
        <Link to="/activities" className="cta-button">체험 둘러보기</Link>
      </section>

      <section className="categories">
        <h2>활동 카테고리</h2>
        <div className="category-grid">
          {categories.map((category) => (
            <div key={category} className="category-card">
              {category}
            </div>
          ))}
        </div>
      </section>

      <section className="featured-activities">
        <h2>인기 체험 활동</h2>
        {loading ? (
          <p>로딩 중...</p>
        ) : activities.length === 0 ? (
          <p>아직 등록된 활동이 없습니다.</p>
        ) : (
          <div className="activity-grid">
            {activities.map((activity) => (
              <Link
                key={activity.id}
                to={`/activities/${activity.id}`}
                className="activity-card"
              >
                <div className="activity-image">
                  {activity.image_url ? (
                    <img src={activity.image_url} alt={activity.title} />
                  ) : (
                    <div className="activity-placeholder">
                      {activity.category}
                    </div>
                  )}
                </div>
                <div className="activity-info">
                  <span className="activity-category">{activity.category}</span>
                  <h3>{activity.title}</h3>
                  <p className="activity-location">📍 {activity.location}</p>
                  <div className="activity-meta">
                    <span>👥 {activity.booking_count || 0}명 신청</span>
                    {activity.duration_minutes && (
                      <span>⏱ {activity.duration_minutes}분</span>
                    )}
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
        <div className="view-all">
          <Link to="/activities" className="view-all-button">
            모든 활동 보기 →
          </Link>
        </div>
      </section>

      <section className="volunteer-section">
        <div className="volunteer-content">
          <h2>🤝 자원봉사자로 함께해주세요</h2>
          <p>
            시니어 분들이 체험 활동을 더욱 즐겁고 안전하게 즐길 수 있도록 
            도와주실 자원봉사자를 모집합니다. 활동에 동행하며 친절하게 안내해주시거나,
            체험 준비를 도와주실 수 있습니다.
          </p>
          <p className="volunteer-benefits">
            <strong>자원봉사자 혜택:</strong> 봉사 시간 인증서 발급, 다양한 체험 활동 무료 참여 기회
          </p>
          <Link to="/activities" className="volunteer-button">
            자원봉사 신청하기 →
          </Link>
        </div>
      </section>
    </div>
  )
}

export default Home

