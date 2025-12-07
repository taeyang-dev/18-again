import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api } from '../api/client'
import './ActivityDetail.css'

function ActivityDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [activity, setActivity] = useState(null)
  const [bookings, setBookings] = useState([])
  const [volunteers, setVolunteers] = useState([])
  const [loading, setLoading] = useState(true)
  const [showBookingForm, setShowBookingForm] = useState(false)
  const [showVolunteerForm, setShowVolunteerForm] = useState(false)
  
  // 예약 폼 상태
  const [bookingForm, setBookingForm] = useState({
    user_id: 1, // 임시 사용자 ID
    notes: ''
  })
  
  // 자원봉사자 폼 상태
  const [volunteerForm, setVolunteerForm] = useState({
    name: '',
    email: '',
    phone: '',
    availability: '',
    experience: ''
  })

  useEffect(() => {
    fetchActivityDetails()
  }, [id])

  const fetchActivityDetails = async () => {
    setLoading(true)
    try {
      const [activityRes, bookingsRes, volunteersRes] = await Promise.all([
        api.getActivity(id),
        api.getActivityBookings(id),
        api.getActivityVolunteers(id)
      ])
      
      setActivity(activityRes.data)
      setBookings(bookingsRes.data)
      setVolunteers(volunteersRes.data)
      setLoading(false)
    } catch (error) {
      console.error('상세 정보 로딩 실패:', error)
      setLoading(false)
    }
  }

  const handleBookingSubmit = async (e) => {
    e.preventDefault()
    try {
      await api.createBooking({
        ...bookingForm,
        activity_id: parseInt(id)
      })
      alert('예약이 완료되었습니다!')
      setShowBookingForm(false)
      fetchActivityDetails()
    } catch (error) {
      alert(error.response?.data?.detail || '예약에 실패했습니다.')
    }
  }

  const handleVolunteerSubmit = async (e) => {
    e.preventDefault()
    try {
      await api.createVolunteer({
        ...volunteerForm,
        activity_id: parseInt(id)
      })
      alert('자원봉사 신청이 완료되었습니다!')
      setShowVolunteerForm(false)
      setVolunteerForm({
        name: '',
        email: '',
        phone: '',
        availability: '',
        experience: ''
      })
      fetchActivityDetails()
    } catch (error) {
      alert(error.response?.data?.detail || '신청에 실패했습니다.')
    }
  }

  if (loading) {
    return <div className="loading">로딩 중...</div>
  }

  if (!activity) {
    return <div className="error">활동을 찾을 수 없습니다.</div>
  }

  return (
    <div className="activity-detail">
      <button onClick={() => navigate(-1)} className="back-button">
        ← 뒤로 가기
      </button>

      <div className="activity-header">
        <div className="activity-image-large">
          {activity.image_url ? (
            <img src={activity.image_url} alt={activity.title} />
          ) : (
            <div className="activity-placeholder-large">
              {activity.category}
            </div>
          )}
        </div>

        <div className="activity-header-info">
          <span className="activity-category">{activity.category}</span>
          <h1>{activity.title}</h1>
          <p className="activity-location">📍 {activity.location}</p>
          {activity.instructor && (
            <p className="activity-instructor">👨‍🏫 강사: {activity.instructor}</p>
          )}
          
          <div className="activity-stats">
            <div className="stat">
              <span className="stat-label">신청자</span>
              <span className="stat-value">{bookings.length}명</span>
            </div>
            {activity.max_participants && (
              <div className="stat">
                <span className="stat-label">최대 인원</span>
                <span className="stat-value">{activity.max_participants}명</span>
              </div>
            )}
            {activity.duration_minutes && (
              <div className="stat">
                <span className="stat-label">소요 시간</span>
                <span className="stat-value">{activity.duration_minutes}분</span>
              </div>
            )}
          </div>

          <div className="activity-actions">
            <button
              onClick={() => setShowBookingForm(!showBookingForm)}
              className="action-button primary"
            >
              체험 신청하기
            </button>
            <button
              onClick={() => setShowVolunteerForm(!showVolunteerForm)}
              className="action-button secondary"
            >
              자원봉사 신청
            </button>
          </div>
        </div>
      </div>

      <div className="activity-content">
        <div className="activity-description-section">
          <h2>활동 소개</h2>
          <p>{activity.description || '상세 설명이 제공되지 않았습니다.'}</p>
        </div>

        {activity.activity_date && (
          <div className="activity-date-section">
            <h2>일시</h2>
            <p>{new Date(activity.activity_date).toLocaleString('ko-KR')}</p>
          </div>
        )}

        <div className="activity-bookings-section">
          <h2>신청자 목록 ({bookings.length}명)</h2>
          {bookings.length === 0 ? (
            <p>아직 신청자가 없습니다.</p>
          ) : (
            <div className="bookings-list">
              {bookings.map((booking) => (
                <div key={booking.id} className="booking-item">
                  <span>예약 #{booking.id}</span>
                  <span>{new Date(booking.booking_date).toLocaleDateString('ko-KR')}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="activity-volunteers-section">
          <h2>자원봉사자 ({volunteers.length}명)</h2>
          {volunteers.length === 0 ? (
            <p>아직 자원봉사자가 없습니다.</p>
          ) : (
            <div className="volunteers-list">
              {volunteers.map((volunteer) => (
                <div key={volunteer.id} className="volunteer-item">
                  <div className="volunteer-info">
                    <h4>{volunteer.name}</h4>
                    <p>{volunteer.email}</p>
                    {volunteer.phone && <p>📞 {volunteer.phone}</p>}
                    {volunteer.availability && (
                      <p>가능 시간: {volunteer.availability}</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {showBookingForm && (
        <div className="modal-overlay" onClick={() => setShowBookingForm(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>체험 신청</h2>
            <form onSubmit={handleBookingSubmit}>
              <div className="form-group">
                <label>사용자 ID</label>
                <input
                  type="number"
                  value={bookingForm.user_id}
                  onChange={(e) =>
                    setBookingForm({ ...bookingForm, user_id: parseInt(e.target.value) })
                  }
                  required
                />
              </div>
              <div className="form-group">
                <label>특별 요청사항</label>
                <textarea
                  value={bookingForm.notes}
                  onChange={(e) =>
                    setBookingForm({ ...bookingForm, notes: e.target.value })
                  }
                  rows="4"
                />
              </div>
              <div className="form-actions">
                <button type="button" onClick={() => setShowBookingForm(false)}>
                  취소
                </button>
                <button type="submit">신청하기</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {showVolunteerForm && (
        <div className="modal-overlay" onClick={() => setShowVolunteerForm(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>자원봉사 신청</h2>
            <form onSubmit={handleVolunteerSubmit}>
              <div className="form-group">
                <label>이름 *</label>
                <input
                  type="text"
                  value={volunteerForm.name}
                  onChange={(e) =>
                    setVolunteerForm({ ...volunteerForm, name: e.target.value })
                  }
                  required
                />
              </div>
              <div className="form-group">
                <label>이메일 *</label>
                <input
                  type="email"
                  value={volunteerForm.email}
                  onChange={(e) =>
                    setVolunteerForm({ ...volunteerForm, email: e.target.value })
                  }
                  required
                />
              </div>
              <div className="form-group">
                <label>전화번호</label>
                <input
                  type="tel"
                  value={volunteerForm.phone}
                  onChange={(e) =>
                    setVolunteerForm({ ...volunteerForm, phone: e.target.value })
                  }
                />
              </div>
              <div className="form-group">
                <label>가능한 시간</label>
                <input
                  type="text"
                  value={volunteerForm.availability}
                  onChange={(e) =>
                    setVolunteerForm({ ...volunteerForm, availability: e.target.value })
                  }
                  placeholder="예: 주중 오전 10시-12시"
                />
              </div>
              <div className="form-group">
                <label>관련 경험</label>
                <textarea
                  value={volunteerForm.experience}
                  onChange={(e) =>
                    setVolunteerForm({ ...volunteerForm, experience: e.target.value })
                  }
                  rows="4"
                  placeholder="관련 경험이나 특기를 입력해주세요"
                />
              </div>
              <div className="form-actions">
                <button type="button" onClick={() => setShowVolunteerForm(false)}>
                  취소
                </button>
                <button type="submit">신청하기</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default ActivityDetail

