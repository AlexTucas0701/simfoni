import React from 'react';

import GitHubSearcher from '../components/GitHubSearcher';
import SearchResult from '../components/SearchResult';


const Home: React.FC = () => {
  return (
    <div className='container'>
      <GitHubSearcher />
      <SearchResult />
    </div>
  )
}

export default Home;
