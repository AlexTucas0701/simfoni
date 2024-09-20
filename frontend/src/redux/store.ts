import { configureStore } from '@reduxjs/toolkit';

import githubSearchReducer from './slices/searchSlice';
import cacheControlReducer from './slices/cacheSlice';


export const store = configureStore({
  reducer: {
    githubSearch: githubSearchReducer,
    cacheControl: cacheControlReducer,
  },
  devTools: true,
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
