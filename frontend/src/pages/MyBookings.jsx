import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api/client'
import './MyBookings.css'

function MyBookings() {
  const [bookings, setBookings] = useState([])
  const [activities, setActivities] = useState({})
  const [loading, setLoading] = useState(true)
  const userId = 1 // 임시 사용자 ID

  useEffect(() => {
    fetchBookings()
  }, [])

  const fetchBookings = async () => {
    setLoading(true)
    try {
      const res = await api.getUserBookings(userId)
      setBookings(res.data)
      
      // 각 예약의 활동 정보 가져오기
      const activityPromises = res.data.map((booking) =>
        api.getActivity(booking.activity_id).catch(() => null)
      )
      const activityRes = await Promise.all(activityPromises)
      
      const activitiesMap = {}
      activityRes.forEach((activityRes, index) => {
        if (activityRes) {
          activitiesMap[res.data[index].activity_id] = activityRes.data
        }
      })
      setActivities(activitiesMap)
      setLoading(false)
    } catch (error) {
      console.error('예약 목록 로딩 실패:', error)
      setLoading(false)
    }
  }

  const handleCancelBooking = async (bookingId) => {
    if (!window.confirm('정말 예약을 취소하시겠습니까?')) {
      return
    }

    try {
      await api.cancelBooking(bookingId)
      alert('예약이 취소되었습니다.')
      fetchBookings()
    } catch (error) {
      alert(error.response?.data?.detail || '예약 취소에 실패했습니다.')
    }
  }

  if (loading) {
    return <div className="loading">로딩 중...</div>
  }

  return (
    <div className="my-bookings">
      <h1>내 예약</h1>
      
      {bookings.length === 0 ? (
        <div className="no-bookings">
          <p>아직 예약한 활동이 없습니다.</p>
          <Link to="/activities" className="browse-activities-button">
            활동 둘러보기
          </Link>
        </div>
      ) : (
        <div className="bookings-list">
          {bookings.map((booking) => {
            const activity = activities[booking.activity_id]
            return (
              <div key={booking.id} className="booking-card">
                {activity ? (
                  <>
                    <div className="booking-activity-info">
                      <Link to={`/activities/${activity.id}`}>
                        <h3>{activity.title}</h3>
                      </Link>
                      <p className="booking-category">{activity.category}</p>
                      <p className="booking-location">📍 {activity.location}</p>
                      {activity.activity_date && (
                        <p className="booking-date">
                          📅 {new Date(activity.activity_date).toLocaleString('ko-KR')}
                        </p>
                      )}
                      {activity.instructor && (
                        <p className="booking-instructor">👨‍🏫 {activity.instructor}</p>
                      )}
                    </div>
                    <div className="booking-meta">
                      <p className="booking-booking-date">
                        예약일: {new Date(booking.booking_date).toLocaleDateString('ko-KR')}
                      </p>
                      {booking.notes && (
                        <p className="booking-notes">
                          <strong>특별 요청:</strong> {booking.notes}
                        </p>
                      )}
                      <button
                        onClick={() => handleCancelBooking(booking.id)}
                        className="cancel-button"
                      >
                        예약 취소
                      </button>
                    </div>
                  </>
                ) : (
                  <p>활동 정보를 불러올 수 없습니다. (ID: {booking.activity_id})</p>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default MyBookings

