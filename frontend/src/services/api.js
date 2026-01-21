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
   * Send a message with streaming logs via SSE
   * @param {string} query - User's message
   * @param {string} sessionId - Session identifier
   * @param {string} icalUrl - Optional iCal URL for timetable
   * @param {Array} conversationHistory - Previous messages for context
   * @param {function} onLog - Callback for log events
   * @param {function} onResponse - Callback for final response
   * @param {function} onError - Callback for errors
   * @param {function} onDone - Callback when stream completes
   * @returns {function} Cleanup function to abort the stream
   */
  streamMessage: (query, sessionId, icalUrl, conversationHistory, { onLog, onResponse, onError, onDone }) => {
    const abortController = new AbortController();

    const fetchStream = async () => {
      try {
        const response = await fetch(`${API_BASE}/chat/stream`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query,
            session_id: sessionId,
            ical_url: icalUrl,
            conversation_history: conversationHistory
          }),
          signal: abortController.signal
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
          const { done, value } = await reader.read();

          if (done) {
            break;
          }

          buffer += decoder.decode(value, { stream: true });

          // Process complete SSE events (separated by \n\n)
          const events = buffer.split('\n\n');
          buffer = events.pop() || ''; // Keep incomplete event in buffer

          for (const event of events) {
            if (event.startsWith('data: ')) {
              try {
                const data = JSON.parse(event.slice(6));

                if (data.type === 'log') {
                  onLog?.(data);
                } else if (data.type === 'response') {
                  onResponse?.(data.content);
                } else if (data.type === 'error') {
                  onError?.(data.message);
                } else if (data.type === 'done') {
                  onDone?.();
                } else if (data.type === 'status') {
                  onLog?.(data);
                }
              } catch (e) {
                console.error('Error parsing SSE event:', e);
              }
            }
          }
        }
      } catch (error) {
        if (error.name !== 'AbortError') {
          console.error('Stream error:', error);
          onError?.(error.message);
        }
      }
    };

    fetchStream();

    // Return cleanup function
    return () => {
      abortController.abort();
    };
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
