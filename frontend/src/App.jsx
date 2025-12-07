import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import Home from './pages/Home'
import Activities from './pages/Activities'
import ActivityDetail from './pages/ActivityDetail'
import MyBookings from './pages/MyBookings'
import './App.css'

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/activities" element={<Activities />} />
            <Route path="/activities/:id" element={<ActivityDetail />} />
            <Route path="/my-bookings" element={<MyBookings />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

