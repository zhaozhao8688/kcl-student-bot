/**
 * TimetableModal component - Modal for syncing timetable via URL or file upload
 */

import React, { useState } from 'react';
import { X, Link2, Upload, Loader2, CheckCircle } from 'lucide-react';

export function TimetableModal({ isOpen, onClose, onSync }) {
  const [url, setUrl] = useState('');
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('idle'); // idle | scanning | success | error
  const [errorMessage, setErrorMessage] = useState('');

  if (!isOpen) return null;

  const handleSync = async (e) => {
    e.preventDefault();

    if (!url && !file) {
      setErrorMessage('Please provide a timetable URL or upload a file');
      return;
    }

    setStatus('scanning');
    setErrorMessage('');

    try {
      // For now, we only support URL. File upload would require backend changes.
      const sourceUrl = file ? file.name : url;
      await onSync(sourceUrl);

      setStatus('success');

      // Close after success
      setTimeout(() => {
        onClose();
        setStatus('idle');
        setUrl('');
        setFile(null);
      }, 1500);
    } catch (error) {
      console.error('Error syncing timetable:', error);
      setStatus('error');
      setErrorMessage('Failed to sync timetable. Please try again.');
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setUrl(''); // Clear URL if file is selected
    }
  };

  const handleClose = () => {
    if (status !== 'scanning') {
      setUrl('');
      setFile(null);
      setStatus('idle');
      setErrorMessage('');
      onClose();
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md transform transition-all">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-200">
          <h2 className="text-xl font-bold text-charcoal">Sync Timetable</h2>
          <button
            onClick={handleClose}
            disabled={status === 'scanning'}
            className="p-1 hover:bg-slate-100 rounded-lg transition-colors disabled:opacity-50"
          >
            <X className="w-5 h-5 text-slate-600" />
          </button>
        </div>

        {/* Content */}
        <form onSubmit={handleSync} className="p-6 space-y-6">
          {/* URL Input */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              <Link2 className="w-4 h-4 inline mr-2" />
              Paste iCal Link
            </label>
            <input
              type="url"
              value={url}
              onChange={(e) => {
                setUrl(e.target.value);
                setFile(null); // Clear file if URL is entered
              }}
              disabled={status === 'scanning' || file !== null}
              placeholder="https://example.com/timetable.ics"
              className="w-full px-4 py-3 border border-slate-200 rounded-xl focus:outline-none focus:border-muted-gold focus:ring-1 focus:ring-muted-gold transition-all disabled:bg-slate-50 disabled:text-slate-400"
            />
          </div>

          {/* Divider */}
          <div className="flex items-center gap-3">
            <div className="flex-1 h-px bg-slate-200"></div>
            <span className="text-xs text-slate-400 font-medium">OR</span>
            <div className="flex-1 h-px bg-slate-200"></div>
          </div>

          {/* File Upload */}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              <Upload className="w-4 h-4 inline mr-2" />
              Upload File
            </label>
            <div className="relative">
              <input
                type="file"
                accept=".ics,.pdf"
                onChange={handleFileChange}
                disabled={status === 'scanning' || url !== ''}
                className="w-full px-4 py-3 border border-slate-200 rounded-xl focus:outline-none focus:border-muted-gold focus:ring-1 focus:ring-muted-gold transition-all disabled:bg-slate-50 disabled:text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-muted-gold/10 file:text-muted-gold hover:file:bg-muted-gold/20"
              />
            </div>
            {file && (
              <p className="mt-2 text-sm text-slate-600">
                Selected: {file.name}
              </p>
            )}
          </div>

          {/* Error Message */}
          {errorMessage && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
              {errorMessage}
            </div>
          )}

          {/* Status Messages */}
          {status === 'scanning' && (
            <div className="flex items-center gap-3 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <Loader2 className="w-5 h-5 text-blue-600 animate-spin" />
              <p className="text-sm text-blue-700 font-medium">
                Scanning your timetable...
              </p>
            </div>
          )}

          {status === 'success' && (
            <div className="flex items-center gap-3 p-4 bg-green-50 border border-green-200 rounded-lg">
              <CheckCircle className="w-5 h-5 text-green-600" />
              <p className="text-sm text-green-700 font-medium">
                Timetable synced successfully!
              </p>
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={status === 'scanning' || (!url && !file)}
            className="w-full py-3 px-6 bg-charcoal hover:bg-black text-white font-medium rounded-xl transition-all disabled:bg-slate-200 disabled:text-slate-400 disabled:cursor-not-allowed active:scale-95"
          >
            {status === 'scanning' ? 'Syncing...' : 'Sync Timetable'}
          </button>
        </form>
      </div>
    </div>
  );
}
