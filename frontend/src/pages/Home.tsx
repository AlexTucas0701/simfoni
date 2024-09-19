import React from 'react';

import GitHubSearcher from '../components/github/GitHubSearcher';
import SearchResult from '../components/github/GitHubSearchResult';


const Home: React.FC = () => {
  return (
    <div className='container'>
      <GitHubSearcher />
      <SearchResult />
    </div>
  )
}

export default Home;
