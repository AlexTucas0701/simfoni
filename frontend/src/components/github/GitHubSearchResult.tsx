import React from 'react';

import Spinner from '../layout/Spinner';
import GitHubRepositoryItem from './GitHubRepositoryItem';
import GitHubSearchError from './GitHubSearchError';
import GitHubUserItem from './GitHubUserItem';
import { SearchType } from '../../types/search';
import type {
  GitHubRepository,
  GitHubSearchParams,
  GitHubSearchResult,
  GitHubUser,
} from '../../types/search';
import { useAppSelector } from '../../hooks';

import '../../css/GitHubSearchResult.css';
import '../../css/GitHubItemCard.css';


const Searching: React.FC<GitHubSearchParams> = ({type, keyword}) => {
  return (
    <>
      <p>Searching GitHub {type} with the keyword: "{keyword}", please wait...</p>
      <Spinner />
    </>
  )
};


const SearchResultPanel: React.FC<GitHubSearchResult> = ({results, search_params}) => {
  if (search_params?.type !== SearchType.USER && search_params?.type !== SearchType.REPO) {
    return (
      <></>
    );
  }

  return (
    <div className="grid-container">
      {results?.map((result) => {
        // Narrowing the type based on search_params.type
        if (search_params.type === SearchType.USER && 'login' in result) {
          return <GitHubUserItem key={result.id} {...result as GitHubUser} />;
        } else if (search_params.type === SearchType.REPO && 'name' in result) {
          return <GitHubRepositoryItem key={result.id} {...result as GitHubRepository} />;
        }
        return null;
      })}
    </div>
  );
};


const SearchResult: React.FC = () => {
  const {
    type: searchType,
    keyword: searchKeyword,
    loading,
    error,
    results,
  } = useAppSelector(state => state.githubSearch);

  return (
    <div className='search-result-container'>
    {
      loading
        ? <Searching type={searchType} keyword={searchKeyword} />
        : error
          ? <GitHubSearchError />
          : results.results
            ? <SearchResultPanel {...results} />
            : <></>
    }
    </div>
  );
};

export default SearchResult;
