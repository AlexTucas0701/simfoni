import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

import { GitHubSearchParams, SearchType, getSearchType } from '../../types/search';
import { useAppDispatch } from '../../hooks/index';
import {
  clearResults as clearResultsRedux,
  fetchGitHubResults,
  setSearchParams as setSearchParamsRedux,
} from '../../redux/slices/searchSlice';

import '../../css/GitHubSearcher.css';


const GitHubSearcher: React.FC = () => {
  const [ searchParams, setSearchParams ] = useSearchParams();

  const search_type = getSearchType(searchParams.get("type") ?? SearchType.USER);
  const init_search_keyword: string = searchParams.get("keyword") ?? "";

  const [ searchKeyword, setSearchKeyword ] = useState<string>(init_search_keyword);
  const [ searchType, setSearchType ] = useState<SearchType>(search_type);

  const navigate = useNavigate();
  const dispatch = useAppDispatch();

  useEffect(() => {
    setSearchParams({
      keyword: searchKeyword,
      type: searchType,
    });
  }, [searchKeyword, searchType, setSearchParams]);

  useEffect(() => {
    const query_string = searchParams.toString();
    const type = getSearchType(searchParams.get("type") ?? "");
    const keyword = searchParams.get("keyword") ?? "";

    navigate(`/?${query_string}`, { replace: true });

    const debounce_timeout_id = setTimeout(() => {
      if (keyword.length < 3) {
        dispatch(clearResultsRedux());
        return;
      }

      const payload: GitHubSearchParams = {
        type,
        keyword,
      };
      dispatch(setSearchParamsRedux(payload));
      dispatch(fetchGitHubResults(payload));
    }, 500);

    return () => {
      clearTimeout(debounce_timeout_id);
    }
  }, [searchParams, navigate, dispatch]);

  const handleSearchKeywordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchKeyword(e.target.value);
  };

  const handleSearchTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    if (!e.target.value) return;
    const newSearchType = getSearchType(e.target.value);
    if (newSearchType) {
      setSearchType(newSearchType);
    }
  };

  return (
    <div className="github-searcher-container">
      <div className="github-searcher">
        <img
          className="github-logo"
          src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
          alt="GitHub Logo"
        />
        <div className="searcher-text">
          <h2>GitHub Searcher</h2>
          <p>Search users or repositories below</p>
        </div>
      </div>

      <div className="search-input-container">
        <input
          type="text"
          className="search-input"
          placeholder="Start typing to search .."
          value={searchKeyword}
          onChange={handleSearchKeywordChange}
        />
        <select className="search-select" value={searchType} onChange={handleSearchTypeChange}>
          <option value={SearchType.USER}>Users</option>
          <option value={SearchType.REPO}>Repositories</option>
        </select>
      </div>
    </div>
  );
};

export default GitHubSearcher;
