import { configureStore } from '@reduxjs/toolkit';

import githubReducer from './features/github/githubSlice';


export const store = configureStore({
  reducer: {
    githubSearch: githubReducer,
  },
  devTools: true,
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
