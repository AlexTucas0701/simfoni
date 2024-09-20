import React from 'react';
import { GitHubUser } from '../../types/search';


const GitHubUserItem: React.FC<GitHubUser> = (user) => {
  return (
    <div className="card">
      <div className="card-title">
        <img
          className="avatar"
          src={user.avatar_url}
          alt={`${user.login} avatar`}
        />
      </div>
      <div className="card-body">
        <a
          href={user.html_url}
          target="_blank"
          rel="noreferrer"
        >
          <h3>{user.login}</h3>
        </a>
      </div>
    </div>
  );
};

export default GitHubUserItem;
