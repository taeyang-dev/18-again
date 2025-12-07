import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api/client'
import './Activities.css'

function Activities() {
  const [activities, setActivities] = useState([])
  const [categories, setCategories] = useState([])
  const [selectedCategory, setSelectedCategory] = useState('')
  const [locationFilter, setLocationFilter] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchActivities()
    fetchCategories()
  }, [selectedCategory, locationFilter])

  const fetchCategories = async () => {
    try {
      const res = await api.getCategories()
      setCategories(res.data.categories)
    } catch (error) {
      console.error('카테고리 로딩 실패:', error)
    }
  }

  const fetchActivities = async () => {
    setLoading(true)
    try {
      const params = {}
      if (selectedCategory) params.category = selectedCategory
      if (locationFilter) params.location = locationFilter

      const res = await api.getActivities(params)
      
      // 각 활동의 예약 수를 가져오기
      const activitiesWithCounts = await Promise.all(
        res.data.map(async (activity) => {
          try {
            const bookingsRes = await api.getActivityBookings(activity.id)
            return {
              ...activity,
              booking_count: bookingsRes.data.length
            }
          } catch {
            return { ...activity, booking_count: 0 }
          }
        })
      )
      
      setActivities(activitiesWithCounts)
      setLoading(false)
    } catch (error) {
      console.error('활동 로딩 실패:', error)
      setLoading(false)
    }
  }

  return (
    <div className="activities-page">
      <h1>체험 활동</h1>
      
      <div className="filters">
        <div className="filter-group">
          <label>카테고리</label>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="filter-select"
          >
            <option value="">전체</option>
            {categories.map((category) => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>지역</label>
          <input
            type="text"
            placeholder="지역명 입력"
            value={locationFilter}
            onChange={(e) => setLocationFilter(e.target.value)}
            className="filter-input"
          />
        </div>

        <button onClick={fetchActivities} className="filter-button">
          검색
        </button>
      </div>

      {loading ? (
        <div className="loading">로딩 중...</div>
      ) : activities.length === 0 ? (
        <div className="no-results">
          <p>조건에 맞는 활동이 없습니다.</p>
        </div>
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
                <p className="activity-description">
                  {activity.description?.substring(0, 100)}...
                </p>
                <p className="activity-location">📍 {activity.location}</p>
                {activity.instructor && (
                  <p className="activity-instructor">👨‍🏫 {activity.instructor}</p>
                )}
                <div className="activity-meta">
                  <span>👥 {activity.booking_count || 0}명 신청</span>
                  {activity.max_participants && (
                    <span>최대 {activity.max_participants}명</span>
                  )}
                  {activity.duration_minutes && (
                    <span>⏱ {activity.duration_minutes}분</span>
                  )}
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}

export default Activities

