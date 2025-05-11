import React, { useState } from 'react';
import axios from 'axios';
import { MicrophoneIcon, StopIcon } from '@heroicons/react/24/solid';

function App() {
  const [narrative, setNarrative] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!narrative.trim()) {
      setError('Please enter an incident narrative');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:5000/api/analyze', {
        narrative
      });
      setRecommendations(response.data.recommendations);
    } catch (err) {
      setError('Error analyzing narrative. Please try again.');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleRecording = () => {
    setIsRecording(!isRecording);
    // TODO: Implement voice recording functionality
  };

  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
          <div className="max-w-md mx-auto">
            <div className="divide-y divide-gray-200">
              <div className="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
                <h1 className="text-3xl font-bold text-center text-primary-600 mb-8">
                  FIR-Assist
                </h1>
                
                <div className="relative">
                  <textarea
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                    rows="6"
                    placeholder="Enter the incident narrative..."
                    value={narrative}
                    onChange={(e) => setNarrative(e.target.value)}
                  />
                  <button
                    onClick={toggleRecording}
                    className="absolute right-2 bottom-2 p-2 rounded-full hover:bg-gray-100"
                  >
                    {isRecording ? (
                      <StopIcon className="h-6 w-6 text-red-500" />
                    ) : (
                      <MicrophoneIcon className="h-6 w-6 text-primary-500" />
                    )}
                  </button>
                </div>

                <button
                  onClick={handleAnalyze}
                  disabled={loading}
                  className="w-full mt-4 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50"
                >
                  {loading ? 'Analyzing...' : 'Analyze'}
                </button>

                {error && (
                  <div className="mt-4 p-3 bg-red-100 text-red-700 rounded-md">
                    {error}
                  </div>
                )}

                {recommendations.length > 0 && (
                  <div className="mt-8 space-y-4">
                    <h2 className="text-xl font-semibold text-gray-900">
                      Recommended IPC Sections
                    </h2>
                    {recommendations.map((rec, index) => (
                      <div
                        key={index}
                        className="p-4 bg-gray-50 rounded-lg border border-gray-200"
                      >
                        <div className="flex justify-between items-start">
                          <div>
                            <h3 className="text-lg font-medium text-primary-600">
                              {rec.code} - {rec.title}
                            </h3>
                            <p className="mt-1 text-gray-600">{rec.description}</p>
                          </div>
                          <span className="px-2 py-1 text-sm bg-primary-100 text-primary-800 rounded">
                            {Math.round(rec.score * 100)}% match
                          </span>
                        </div>
                        
                        {rec.judgments.length > 0 && (
                          <div className="mt-4">
                            <h4 className="text-sm font-medium text-gray-900">
                              Related Judgments:
                            </h4>
                            <ul className="mt-2 space-y-2">
                              {rec.judgments.map((judgment, jIndex) => (
                                <li
                                  key={jIndex}
                                  className="text-sm text-gray-600"
                                >
                                  <span className="font-medium">
                                    {judgment.caseName}:
                                  </span>{' '}
                                  {judgment.synopsis}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App; 