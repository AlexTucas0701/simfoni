import React, { useEffect, useState } from 'react';
import { useNavigate, useParams, useSearchParams } from 'react-router-dom';

import { SearchType, getSearchType } from '../types/search';

import '../css/GitHubSearcher.css';


const GitHubSearcher: React.FC = () => {
  const { type } = useParams();
  const [ searchParams, setSearchParams ] = useSearchParams();

  const search_type = getSearchType(type ?? SearchType.USER) ?? SearchType.USER;
  const init_search_keyword: string = searchParams.get("keyword") ?? "";

  const [ searchKeyword, setSearchKeyword ] = useState<string>(init_search_keyword);
  const [ searchType, setSearchType ] = useState<SearchType>(search_type);

  const navigate = useNavigate();

  useEffect(() => {
    setSearchParams({
      keyword: searchKeyword,
    });
  }, [searchKeyword]);

  useEffect(() => {
    const query_string = searchParams.toString();
    navigate(`/${searchType}?${query_string}`, { replace: true });
  }, [searchParams, searchType]);

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
          <option value={SearchType.ISSUE}>Issues</option>
        </select>
      </div>
    </div>
  );
};

export default GitHubSearcher;
