import React from 'react';

import { clearGitHubSearchRemoteCache } from '../../redux/slices/cacheSlice';
import { useAppDispatch, useAppSelector } from '../../hooks';

import '../../css/GitHubSearchCacheControl.css';


const GitHubSearchCacheControl: React.FC = () => {
  const dispatch = useAppDispatch();
  const clear_cache_state = useAppSelector(state => state.cacheControl);

  const onClickCleanRemote = () => {
    dispatch(clearGitHubSearchRemoteCache());
  };

  return (
    <div className="github-search-cache-control-container">
      <span>Clear the cache:</span>
      <button>Local</button>
      <button
        onClick={onClickCleanRemote}
        disabled={clear_cache_state.cleaning}
      >
        {
          clear_cache_state.cleaning
            ? "..."
            : "Remote"
        }
      </button>
    </div>
  );
};

export default GitHubSearchCacheControl;
