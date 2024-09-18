import axios from 'axios';
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';

// import type { RootState } from '../../store';
import { SearchType } from '../../types/search';

interface GitHubSearchState {
  type: SearchType;
  keyword: string;
  results: any[];
  loading: boolean;
  error: string | null;
}

interface GitHubSearchParams {
  type: SearchType;
  keyword: string;
}

const initialState: GitHubSearchState = {
  type: SearchType.USER,
  keyword: '',
  results: [],
  loading: false,
  error: null,
}

export const fetchGitHubResults = createAsyncThunk(
  'githubSearch/fetchResults',
  async ({ type, keyword }: GitHubSearchParams) => {
    const response = await axios.get(
      `https://api.github.com/search/${type}?q=${keyword}`
    );
    return response.data.items; // GitHub API returns items in the response
  },
);

export const githubSlice = createSlice({
  name: 'gihtub',
  initialState,
  reducers: {
    setSearchParams(state, action: PayloadAction<GitHubSearchParams>) {
      state.keyword = action.payload.keyword;
      state.type = action.payload.type;
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

export const { setSearchParams } = githubSlice.actions;

export default githubSlice.reducer;
