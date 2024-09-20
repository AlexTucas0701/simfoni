import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

// import type { RootState } from '../../store';
import {
  GitHubSearchParams,
  GitHubSearchState,
  SearchType,
} from '../../types/search';
import api from '../../utils/api';


const initialState: GitHubSearchState = {
  type: SearchType.USER,
  keyword: '',
  results: {},
  loading: false,
  error: null,
};


export const fetchGitHubResults = createAsyncThunk(
  'githubSearch/fetchResults',
  async ({ type, keyword }: GitHubSearchParams) => {
    const response = await api.post(
      "/search",
      {
        type: type,
        keyword: keyword,
      },
    );
    return response.data;
  },
);

export const githubSearchSlice = createSlice({
  name: 'gihtub',
  initialState,
  reducers: {
    setSearchParams(state, action: PayloadAction<GitHubSearchParams>) {
      state.keyword = action.payload.keyword;
      state.type = action.payload.type;
    },
    clearResults(state) {
      state.results = {}
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchGitHubResults.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchGitHubResults.fulfilled, (state, action) => {
        state.loading = false;
        state.results = action.payload;
      })
      .addCase(fetchGitHubResults.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Something went wrong';
      });
  },
});

export const { setSearchParams, clearResults } = githubSearchSlice.actions;

export default githubSearchSlice.reducer;
