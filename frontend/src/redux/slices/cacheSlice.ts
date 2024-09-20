import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

import api from '../../utils/api';

interface ClearCacheState {
  cleaning: boolean;
  error: string | null;
}

const initialState: ClearCacheState = {
  cleaning: false,
  error: null,
};

export const clearGitHubSearchRemoteCache = createAsyncThunk(
  'githubSearch/clearRemoteCache',
  async () => {
    await api.get(
      "/clear-cache",
    );
    return;
  },
);

export const clearGitHubSearchRemoteCacheSlice = createSlice({
  name: 'cache',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
    .addCase(clearGitHubSearchRemoteCache.pending, (state) => {
      state.cleaning = true;
      state.error = null;
    })
    .addCase(clearGitHubSearchRemoteCache.fulfilled, (state) => {
      state.cleaning = false;
      state.error = null;
    })
    .addCase(clearGitHubSearchRemoteCache.rejected, (state, action) => {
      state.cleaning = false;
      state.error = action.error.message || "Something went wrong";
    });
  }
})

export const {} = clearGitHubSearchRemoteCacheSlice.actions;

export default clearGitHubSearchRemoteCacheSlice.reducer;
