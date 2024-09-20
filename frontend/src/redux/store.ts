import { configureStore } from '@reduxjs/toolkit';
import storage from 'redux-persist/lib/storage';
import {
  persistStore,
  persistReducer,
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER,
} from 'redux-persist'
import { combineReducers } from 'redux';

import githubSearchReducer from './slices/searchSlice';
import cacheControlReducer from './slices/cacheSlice';


// Create a persist config specifically for the cache slice
const cachePersistConfig = {
  key: 'cacheControl',
  storage,
  whitelist: ['cached'],
};

// Wrap cacheControlReducer with persistReducer
const persistedCacheControlReducer = persistReducer(cachePersistConfig, cacheControlReducer);

export const store = configureStore({
  reducer: combineReducers({
    githubSearch: githubSearchReducer,
    cacheControl: persistedCacheControlReducer,
  }),
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    }),
  devTools: true,
});

// Persistor
export const persistor = persistStore(store);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
