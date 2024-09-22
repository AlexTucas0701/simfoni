import { configureStore } from '@reduxjs/toolkit';
import storage from 'redux-persist/lib/storage'; // Default storage engine (localStorage)
import {
  persistStore,
  persistReducer,
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER,
} from 'redux-persist';
import { combineReducers } from 'redux';

import githubSearchReducer from './slices/searchSlice'; // Reducer for handling GitHub search functionality
import cacheControlReducer from './slices/cacheSlice'; // Reducer for managing cache state

// Create a persist config specifically for the cache slice
// This configuration is used to tell redux-persist how to handle the cache slice.
const cachePersistConfig = {
  key: 'cacheControl', // Key used for storing cache slice in localStorage
  storage, // Specifies that we are using localStorage
  whitelist: ['cached'], // Only persist the 'cached' part of the state
};

// Wrap cacheControlReducer with persistReducer
// This will ensure that the cache state is saved to and loaded from localStorage.
const persistedCacheControlReducer = persistReducer(cachePersistConfig, cacheControlReducer);

// Configure the Redux store
export const store = configureStore({
  reducer: combineReducers({
    githubSearch: githubSearchReducer, // Register the GitHub search reducer
    cacheControl: persistedCacheControlReducer, // Register the persisted cache control reducer
  }),
  middleware: (getDefaultMiddleware) =>
    // Add middleware for redux-persist while ensuring it plays nicely with serializable checks
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER], // Ignore these redux-persist actions in serializability checks
      },
    }),
  devTools: true, // Enable Redux DevTools for easier debugging
});

// Persistor is used to persist the store data to localStorage
export const persistor = persistStore(store);

// Type definitions for the root state and dispatch
export type RootState = ReturnType<typeof store.getState>; // Defines the RootState type based on the store's state structure
export type AppDispatch = typeof store.dispatch; // Defines the AppDispatch type for dispatching actions
