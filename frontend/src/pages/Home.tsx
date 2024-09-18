import React from 'react';
import { Navigate, useParams } from 'react-router-dom';

import GitHubSearcher from '../components/GitHubSearcher';
import SearchResult from '../components/SearchResult';
import { getSearchType } from '../types/search';


const Home: React.FC = () => {
  const { type } = useParams();

  if (type === undefined || getSearchType(type) === undefined) {
    return (<Navigate to="/" />);
  }

  return (
    <div className='container'>
      <GitHubSearcher />
      <SearchResult />
    </div>
  )
}

export default Home;
