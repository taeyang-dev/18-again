import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import './Header.css'

function Header() {
  const navigate = useNavigate()

  return (
    <header className="header">
      <div className="header-container">
        <Link to="/" className="logo">
          <h1>시니어 체험 플랫폼</h1>
        </Link>
        <nav className="nav">
          <Link to="/" className="nav-link">홈</Link>
          <Link to="/activities" className="nav-link">체험 활동</Link>
          <Link to="/my-bookings" className="nav-link">내 예약</Link>
        </nav>
      </div>
    </header>
  )
}

export default Header

