import React from 'react';

import { useAppSelector } from '../../hooks';
import Spinner from '../layout/Spinner';

import '../../css/SearchResult.css';
import { SearchType } from '../../types/search';


interface SearchingProps {
  type: SearchType;
  keyword: string;
}


const Searching: React.FC<SearchingProps> = ({type, keyword}) => {
  return (
    <>
      <p>Searching GitHub {type} with the keyword: "{keyword}", please wait...</p>
      <Spinner />
    </>
  )
};


const SearchResult: React.FC = () => {
  const {
    type: searchType,
    keyword: searchKeyword,
    loading,
    // error,
    // results,
  } = useAppSelector(state => state.githubSearch);

  return (
    <div className='search-result-container'>
    {
      loading
        ? <Searching type={searchType} keyword={searchKeyword} />
        : <div>OK</div>
    }
    </div>
  );
};

export default SearchResult;
