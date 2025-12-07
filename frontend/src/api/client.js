import axios from 'axios'

const API_BASE_URL = 'https://one8-again-backend.onrender.com/api'

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const api = {
  // Activities
  getActivities: (params) => client.get('/activities', { params }),
  getActivity: (id) => client.get(`/activities/${id}`),
  createActivity: (data) => client.post('/activities', data),
  
  // Bookings
  createBooking: (data) => client.post('/bookings', data),
  getUserBookings: (userId) => client.get(`/users/${userId}/bookings`),
  getActivityBookings: (activityId) => client.get(`/activities/${activityId}/bookings`),
  cancelBooking: (bookingId) => client.delete(`/bookings/${bookingId}`),
  
  // Volunteers
  createVolunteer: (data) => client.post('/volunteers', data),
  getActivityVolunteers: (activityId) => client.get(`/activities/${activityId}/volunteers`),
  
  // Users
  createUser: (data) => client.post('/users', data),
  getUser: (userId) => client.get(`/users/${userId}`),
  
  // Subscriptions
  createSubscription: (data) => client.post('/subscriptions', data),
  getUserSubscription: (userId) => client.get(`/users/${userId}/subscription`),
  
  // Categories
  getCategories: () => client.get('/categories'),
}

export default client

