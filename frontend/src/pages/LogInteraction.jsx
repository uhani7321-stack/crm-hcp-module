import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { updateField, populateFromAI } from '../redux/slices/interactionSlice';
import { addMessage } from '../redux/slices/chatSlice';
import { setLoading, setError } from '../redux/slices/loadingSlice';
import { extractFromChat } from '../services/api';
import { 
  Bot, Search, Calendar, Clock, Mic, Sparkles, Box, 
  Smile, Meh, Frown, Send 
} from 'lucide-react';

const LogInteraction = () => {
  const dispatch = useDispatch();
  const formData = useSelector((state) => state.interaction);
  const chatMessages = useSelector((state) => state.chat.messages);
  const isLoading = useSelector((state) => state.loading.isLoading);
  
  const [chatInput, setChatInput] = useState('');

  const handleInputChange = (field, value) => {
    dispatch(updateField({ field, value }));
  };

  const handleLogChat = async () => {
    if (!chatInput.trim()) return;
    
    const userMsg = chatInput;
    setChatInput('');
    dispatch(addMessage({ role: 'user', content: userMsg }));
    dispatch(setLoading(true));
    
    try {
      const data = await extractFromChat(userMsg);
      if (data && data.summary && data.summary.includes('Missing GROQ_API_KEY')) {
        dispatch(addMessage({ 
          role: 'assistant', 
          content: 'Error: The AI extraction failed because your GROQ_API_KEY is missing in the backend/.env file. Please add it and try again.' 
        }));
      } else if (data && data.summary && data.summary.includes('LLM Error')) {
        dispatch(addMessage({ 
          role: 'assistant', 
          content: `Error from Groq: ${data.summary}` 
        }));
      } else if (data) {
        dispatch(populateFromAI(data));
        
        let responseContent = data.summary || "Extracted details from your message and populated the form.";
        
        dispatch(addMessage({ 
          role: 'assistant', 
          content: responseContent 
        }));
      }
    } catch (error) {
      dispatch(setError(error.message));
      dispatch(addMessage({ 
        role: 'assistant', 
        content: 'Failed to extract data. Is the backend running?' 
      }));
    } finally {
      dispatch(setLoading(false));
    }
  };

  return (
    <div className="flex flex-col lg:flex-row gap-6">
      {/* Left Section - Interaction Details (70%) */}
      <div className="w-full lg:w-[70%] bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden flex flex-col">
        <div className="px-6 py-4 border-b border-gray-100">
          <h2 className="text-[15px] font-semibold text-gray-800">Interaction Details</h2>
        </div>
        
        <div className="p-6 flex flex-col gap-5">
          {/* Row 1 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <label className="text-[13px] font-medium text-gray-700">HCP Name</label>
              <div className="relative">
                <input 
                  type="text" 
                  placeholder="Search or select HCP..." 
                  className="w-full border border-gray-300 rounded-md py-2 pl-3 pr-10 text-[14px] focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                  value={formData.hcp_name}
                  onChange={(e) => handleInputChange('hcp_name', e.target.value)}
                />
              </div>
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="text-[13px] font-medium text-gray-700">Interaction Type</label>
              <select 
                className="w-full border border-gray-300 rounded-md py-2 px-3 text-[14px] focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary bg-white"
                value={formData.interaction_type}
                onChange={(e) => handleInputChange('interaction_type', e.target.value)}
              >
                <option value="Meeting">Meeting</option>
                <option value="Call">Call</option>
                <option value="Email">Email</option>
                <option value="Conference">Conference</option>
              </select>
            </div>
          </div>

          {/* Row 2 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <label className="text-[13px] font-medium text-gray-700">Date</label>
              <div className="relative">
                <input 
                  type="date" 
                  className="w-full border border-gray-300 rounded-md py-2 px-3 text-[14px] focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                  value={formData.date}
                  onChange={(e) => handleInputChange('date', e.target.value)}
                />
              </div>
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="text-[13px] font-medium text-gray-700">Time</label>
              <div className="relative">
                <input 
                  type="time" 
                  className="w-full border border-gray-300 rounded-md py-2 px-3 text-[14px] focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                  value={formData.time}
                  onChange={(e) => handleInputChange('time', e.target.value)}
                />
              </div>
            </div>
          </div>

          {/* Row 3 */}
          <div className="flex flex-col gap-1.5">
            <label className="text-[13px] font-medium text-gray-700">Attendees</label>
            <input 
              type="text" 
              placeholder="Enter names or search..." 
              className="w-full border border-gray-300 rounded-md py-2 px-3 text-[14px] focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
              value={formData.attendees}
              onChange={(e) => handleInputChange('attendees', e.target.value)}
            />
          </div>

          {/* Row 4 */}
          <div className="flex flex-col gap-1.5 relative">
            <label className="text-[13px] font-medium text-gray-700">Topics Discussed</label>
            <textarea 
              rows={4}
              placeholder="Enter key discussion points..." 
              className="w-full border border-gray-300 rounded-md py-2 px-3 text-[14px] focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary resize-y"
              value={formData.topics_discussed}
              onChange={(e) => handleInputChange('topics_discussed', e.target.value)}
            />
            <button className="absolute bottom-3 right-3 text-gray-400 hover:text-gray-600">
              <Mic size={18} />
            </button>
          </div>
          
          <div>
            <button className="flex items-center gap-2 bg-gray-50 border border-gray-200 text-gray-700 px-4 py-1.5 rounded-md text-[13px] font-medium hover:bg-gray-100 transition-colors">
              <Sparkles size={14} className="text-gray-500" />
              Summarize from Voice Note (Requires Consent)
            </button>
          </div>

          {/* Materials & Samples */}
          <div className="mt-2 flex flex-col gap-3">
            <h3 className="text-[14px] font-medium text-gray-700">Materials Shared / Samples Distributed</h3>
            
            <div className="flex justify-between items-center border border-gray-200 rounded-md p-3">
              <div>
                <div className="text-[13px] font-medium text-gray-800">Materials Shared</div>
                <div className="text-[12px] text-gray-500 mt-0.5">
                  {formData.materials_shared && formData.materials_shared.length > 0
                    ? (Array.isArray(formData.materials_shared) ? formData.materials_shared.join(', ') : formData.materials_shared)
                    : <span className="italic">No materials added.</span>}
                </div>
              </div>
              <button className="flex items-center gap-1.5 border border-gray-300 px-3 py-1.5 rounded-md text-[13px] font-medium text-gray-700 hover:bg-gray-50 bg-white shadow-sm">
                <Search size={14} /> Search/Add
              </button>
            </div>
            
            <div className="flex justify-between items-center border border-gray-200 rounded-md p-3">
              <div>
                <div className="text-[13px] font-medium text-gray-800">Samples Distributed</div>
                <div className="text-[12px] text-gray-500 mt-0.5">
                  {formData.samples_distributed && formData.samples_distributed.length > 0
                    ? (Array.isArray(formData.samples_distributed) ? formData.samples_distributed.join(', ') : formData.samples_distributed)
                    : <span className="italic">No samples added.</span>}
                </div>
              </div>
              <button className="flex items-center gap-1.5 border border-gray-300 px-3 py-1.5 rounded-md text-[13px] font-medium text-gray-700 hover:bg-gray-50 bg-white shadow-sm">
                <Box size={14} /> Add Sample
              </button>
            </div>
          </div>

          {/* Sentiment */}
          <div className="mt-2 flex flex-col gap-2">
            <h3 className="text-[14px] font-medium text-gray-700">Observed/Inferred HCP Sentiment</h3>
            <div className="flex items-center gap-6 mt-1">
              <label className="flex items-center gap-2 cursor-pointer group">
                <input 
                  type="radio" 
                  name="sentiment" 
                  value="Positive" 
                  checked={formData.sentiment === 'Positive'}
                  onChange={() => handleInputChange('sentiment', 'Positive')}
                  className="w-4 h-4 text-primary focus:ring-primary border-gray-300"
                />
                <div className="flex flex-col items-center">
                  <Smile size={20} className={formData.sentiment === 'Positive' ? 'text-primary' : 'text-gray-400 group-hover:text-gray-500'} />
                  <span className="text-[13px] text-gray-700 mt-1">Positive</span>
                </div>
              </label>
              
              <label className="flex items-center gap-2 cursor-pointer group">
                <input 
                  type="radio" 
                  name="sentiment" 
                  value="Neutral" 
                  checked={formData.sentiment === 'Neutral'}
                  onChange={() => handleInputChange('sentiment', 'Neutral')}
                  className="w-4 h-4 text-primary focus:ring-primary border-gray-300"
                />
                <div className="flex flex-col items-center">
                  <Meh size={20} className={formData.sentiment === 'Neutral' ? 'text-primary' : 'text-gray-400 group-hover:text-gray-500'} />
                  <span className="text-[13px] text-gray-700 mt-1">Neutral</span>
                </div>
              </label>

              <label className="flex items-center gap-2 cursor-pointer group">
                <input 
                  type="radio" 
                  name="sentiment" 
                  value="Negative" 
                  checked={formData.sentiment === 'Negative'}
                  onChange={() => handleInputChange('sentiment', 'Negative')}
                  className="w-4 h-4 text-primary focus:ring-primary border-gray-300"
                />
                <div className="flex flex-col items-center">
                  <Frown size={20} className={formData.sentiment === 'Negative' ? 'text-primary' : 'text-gray-400 group-hover:text-gray-500'} />
                  <span className="text-[13px] text-gray-700 mt-1">Negative</span>
                </div>
              </label>
            </div>
          </div>

          {/* Outcomes */}
          <div className="flex flex-col gap-1.5 mt-2">
            <label className="text-[13px] font-medium text-gray-700">Outcomes</label>
            <textarea 
              rows={3}
              placeholder="Key outcomes or agreements..." 
              className="w-full border border-gray-300 rounded-md py-2 px-3 text-[14px] focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary resize-y"
              value={formData.outcomes}
              onChange={(e) => handleInputChange('outcomes', e.target.value)}
            />
          </div>

          {/* Follow-up Actions */}
          <div className="flex flex-col gap-1.5 mt-2">
            <label className="text-[13px] font-medium text-gray-700">Follow-up Actions</label>
            <textarea 
              rows={3}
              placeholder="Enter next steps or tasks..." 
              className="w-full border border-gray-300 rounded-md py-2 px-3 text-[14px] focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary resize-y"
              value={formData.follow_up_actions}
              onChange={(e) => handleInputChange('follow_up_actions', e.target.value)}
            />
          </div>

          {/* AI Suggested Follow-ups */}
          <div className="mt-1">
            <h3 className="text-[13px] font-medium text-gray-700 mb-2">AI Suggested Follow-ups:</h3>
            <div className="flex flex-col gap-1.5">
              <button className="text-left text-primary text-[13px] hover:underline hover:text-blue-700 transition-colors w-fit">
                + Schedule follow-up meeting in 2 weeks
              </button>
              <button className="text-left text-primary text-[13px] hover:underline hover:text-blue-700 transition-colors w-fit">
                + Send OncoBoost Phase III PDF
              </button>
              <button className="text-left text-primary text-[13px] hover:underline hover:text-blue-700 transition-colors w-fit">
                + Add Dr. Sharma to advisory board invite list
              </button>
            </div>
          </div>

        </div>
      </div>

      {/* Right Section - AI Assistant (30%) */}
      <div className="w-full lg:w-[30%] bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden flex flex-col h-[calc(100vh-120px)] lg:h-auto min-h-[600px]">
        {/* Header */}
        <div className="px-5 py-4 border-b border-gray-100 flex items-center gap-2">
          <div className="bg-blue-100 text-primary p-1.5 rounded-md">
            <Bot size={18} />
          </div>
          <div>
            <h2 className="text-[14px] font-semibold text-gray-800">AI Assistant</h2>
            <p className="text-[12px] text-gray-500">Log interaction details here via chat</p>
          </div>
        </div>
        
        {/* Chat Area */}
        <div className="flex-1 p-4 bg-[#FAFAFA] flex flex-col overflow-y-auto">
          {/* Default Info Card */}
          {chatMessages.length === 0 && (
            <div className="bg-[#e6f4f1] text-[#2c7a7b] rounded-lg p-4 text-[13px] shadow-sm leading-relaxed mb-4">
              Log interaction details here (e.g., "Met Dr. Smith, discussed Prodo-X efficacy, positive sentiment, shared brochure") or ask for help.
            </div>
          )}
          
          {/* Messages */}
          <div className="mt-4 flex flex-col gap-4">
            {chatMessages.map((msg, idx) => (
              <div 
                key={idx} 
                className={`max-w-[90%] rounded-lg p-3 text-[13px] shadow-sm ${
                  msg.role === 'user' 
                    ? 'bg-blue-600 text-white self-end rounded-tr-none' 
                    : 'bg-[#e8f5e9] text-[#2e7d32] border border-[#c8e6c9] self-start rounded-tl-none'
                }`}
              >
                {msg.role === 'assistant' ? (
                  <div className="flex flex-col gap-1">
                    <div className="flex items-start gap-1.5">
                      <span className="text-green-600">✅</span>
                      <span>{msg.content}</span>
                    </div>
                  </div>
                ) : (
                  msg.content
                )}
              </div>
            ))}
            {isLoading && (
              <div className="bg-white border border-gray-200 text-gray-500 self-start rounded-lg rounded-tl-none shadow-sm p-3 text-[13px] flex items-center gap-2">
                <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            )}
          </div>
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-gray-200 bg-white">
          <div className="flex gap-2">
            <input 
              type="text" 
              placeholder="Describe interaction..." 
              className="flex-1 border border-gray-300 rounded-md py-2 px-3 text-[13px] focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') handleLogChat();
              }}
            />
            <button 
              className="bg-primary hover:bg-blue-700 text-white p-2 rounded-md transition-colors flex items-center justify-center min-w-[40px] disabled:opacity-50"
              onClick={handleLogChat}
              disabled={isLoading || !chatInput.trim()}
            >
              <Send size={16} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LogInteraction;
