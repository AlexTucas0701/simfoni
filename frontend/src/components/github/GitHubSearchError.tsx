import React from 'react';

interface GitHubSearchError {
  error: string;
}


const GitHubSearchError: React.FC<GitHubSearchError> = ({error}) => {
  return (
    <>{error}</>
  );
};

export default GitHubSearchError;
