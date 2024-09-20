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
          {
            repository.description
              && <p
                style={{
                  textAlign: "left"
                }}
              >
                {repository.description}
              </p>
          }
        </a>
      </div>
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
        {repository.stargazers_count}
      </div>
    </div>
  );
};

export default GitHubRepositoryItem;
