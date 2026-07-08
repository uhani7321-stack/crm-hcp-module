import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  hcp_name: '',
  interaction_type: 'Meeting',
  date: '',
  time: '',
  attendees: '',
  topics_discussed: '',
  materials_shared: '',
  samples_distributed: '',
  sentiment: '',
  outcomes: '',
  follow_up_actions: '',
};

const interactionSlice = createSlice({
  name: 'interaction',
  initialState,
  reducers: {
    updateField: (state, action) => {
      const { field, value } = action.payload;
      if (field in state) {
        state[field] = value;
      }
    },
    populateFromAI: (state, action) => {
      const data = action.payload;
      
      const safeJoin = (val, separator = ', ') => {
        if (!val) return '';
        if (Array.isArray(val)) return val.join(separator);
        return String(val);
      };

      return {
        ...state,
        hcp_name: data.hcp_name || state.hcp_name,
        interaction_type: data.interaction_type || state.interaction_type,
        date: data.date || state.date,
        time: data.time || state.time,
        attendees: safeJoin(data.attendees, ', ') || state.attendees,
        topics_discussed: safeJoin(data.topics_discussed, '\n') || state.topics_discussed,
        materials_shared: safeJoin(data.materials_shared, ', ') || state.materials_shared,
        samples_distributed: safeJoin(data.samples_distributed, ', ') || state.samples_distributed,
        sentiment: data.sentiment || state.sentiment,
        outcomes: data.outcomes || state.outcomes,
        follow_up_actions: data.follow_up_actions || state.follow_up_actions,
      };
    },
    resetForm: () => initialState,
  },
});

export const { updateField, populateFromAI, resetForm } = interactionSlice.actions;
export default interactionSlice.reducer;
