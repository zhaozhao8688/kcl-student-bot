/**
 * API service for communicating with the FastAPI backend
 */

import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

/**
 * Chat API endpoints
 */
export const chatAPI = {
  /**
   * Send a message to the chat API
   * @param {string} query - User's message
   * @param {string} sessionId - Session identifier
   * @param {string} icalUrl - Optional iCal URL for timetable
   * @returns {Promise} API response with AI message and session ID
   */
  sendMessage: async (query, sessionId, icalUrl) => {
    try {
      const res = await axios.post(`${API_BASE}/chat/message`, {
        query,
        session_id: sessionId,
        ical_url: icalUrl
      });
      return res.data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  },

  /**
   * Get chat history for a session
   * @param {string} sessionId - Session identifier
   * @returns {Promise} Array of messages
   */
  getHistory: async (sessionId) => {
    try {
      const res = await axios.get(`${API_BASE}/chat/history/${sessionId}`);
      return res.data;
    } catch (error) {
      console.error('Error getting history:', error);
      throw error;
    }
  }
};

/**
 * Timetable API endpoints
 */
export const timetableAPI = {
  /**
   * Set the iCal URL for a session
   * @param {string} sessionId - Session identifier
   * @param {string} icalUrl - iCal URL
   * @returns {Promise} Success response
   */
  setUrl: async (sessionId, icalUrl) => {
    try {
      const res = await axios.post(`${API_BASE}/timetable/set-url`, {
        session_id: sessionId,
        ical_url: icalUrl
      });
      return res.data;
    } catch (error) {
      console.error('Error setting timetable URL:', error);
      throw error;
    }
  },

  /**
   * Get the iCal URL for a session
   * @param {string} sessionId - Session identifier
   * @returns {Promise} Timetable URL response
   */
  getUrl: async (sessionId) => {
    try {
      const res = await axios.get(`${API_BASE}/timetable/get-url/${sessionId}`);
      return res.data;
    } catch (error) {
      console.error('Error getting timetable URL:', error);
      throw error;
    }
  }
};

/**
 * Session API endpoints
 */
export const sessionAPI = {
  /**
   * Create a new session
   * @returns {Promise} New session ID
   */
  create: async () => {
    try {
      const res = await axios.post(`${API_BASE}/session/create`);
      return res.data;
    } catch (error) {
      console.error('Error creating session:', error);
      throw error;
    }
  },

  /**
   * Get session status
   * @param {string} sessionId - Session identifier
   * @returns {Promise} Session status information
   */
  getStatus: async (sessionId) => {
    try {
      const res = await axios.get(`${API_BASE}/session/status/${sessionId}`);
      return res.data;
    } catch (error) {
      console.error('Error getting session status:', error);
      throw error;
    }
  }
};
