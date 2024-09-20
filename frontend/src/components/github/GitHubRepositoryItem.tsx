import React from 'react';
import { GitHubRepository } from '../../types/search';


const GitHubRepositoryItem: React.FC<GitHubRepository> = (repository) => {
  return (
    <div className="card">
      <div className="card-title">
        <a
          href={repository.html_url}
          target="_blank"
          rel="noreferrer"
        >
          <h2>{repository.name}</h2>
        </a>
      </div>
      {/* {
        repository.description
          && <p>
            {repository.description}
          </p>
      } */}
      <div className="card-body">
        <h3>Owner</h3>
        <div
          style={{
            marginLeft: "20px"
          }}
        >
          <div>
            <img
              className="avatar"
              src={repository.owner.avatar_url}
              alt={`${repository.owner.login} avatar`}
            />
          </div>
          <div>
            <a
              href={repository.owner.html_url}
              target="_blank"
              rel="noreferrer"
            >
              <h3>{repository.owner.login}</h3>
            </a>
          </div>
        </div>
        <div className="card-footer">
          <span>⭐ {repository.stargazers_count}</span>
          <span>👁️ {repository.watchers_count}</span>
          <span>🍴 {repository.forks_count}</span>
          <span>❗ {repository.open_issues_count}</span>
        </div>
      </div>
    </div>
  );
};

export default GitHubRepositoryItem;
