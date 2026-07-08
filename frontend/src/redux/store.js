import { configureStore } from '@reduxjs/toolkit';
import interactionReducer from './slices/interactionSlice';
import chatReducer from './slices/chatSlice';
import loadingReducer from './slices/loadingSlice';

export const store = configureStore({
  reducer: {
    interaction: interactionReducer,
    chat: chatReducer,
    loading: loadingReducer,
  },
});
