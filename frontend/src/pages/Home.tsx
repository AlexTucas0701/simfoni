import React from 'react';

import GitHubSearcher from '../components/github/GitHubSearcher';
import SearchResult from '../components/github/GitHubSearchResult';
import GitHubSearchCacheControl from '../components/github/GitHubSearchCacheControl';


const Home: React.FC = () => {
  return (
    <div className='container'>
      <GitHubSearcher />
      <GitHubSearchCacheControl />
      <SearchResult />
    </div>
  )
}

export default Home;
