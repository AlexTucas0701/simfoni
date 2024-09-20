import { createAsyncThunk, createSlice, PayloadAction } from '@reduxjs/toolkit';

import api from '../../utils/api';
import { GitHubSearchParams } from '../../types/search';

interface ClearCacheState {
  cleaning: boolean;
  error: string | null;
  cached: any;
}

const initialState: ClearCacheState = {
  cleaning: false,
  error: null,
  cached: {},
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
  reducers: {
    storeCache(state, action: PayloadAction<{search_params: GitHubSearchParams, results: any}>) {
      const search_params = action.payload.search_params;
      if (state.cached[search_params.type] === undefined) state.cached[search_params.type] = {};
      state.cached[search_params.type][search_params.keyword] = action.payload.results;
    },
    clearCache(state) {
      state.cached = {};
    },
  },
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

export const { storeCache, clearCache } = clearGitHubSearchRemoteCacheSlice.actions;

export default clearGitHubSearchRemoteCacheSlice.reducer;
