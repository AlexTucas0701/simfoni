export const enum SearchType {
  USER = "user",
  REPO = "repo",
  ISSUE = "issue",
}


export interface GitHubSearchParams {
  type: SearchType;
  keyword: string;
}


export interface GitHubSearchState extends GitHubSearchParams {
  results: GitHubSearchResult;
  loading: boolean;
  error: string | null;
}


export interface GitHubLicense {
  key: string;
  name: string;
  spdx_id: string;
  url?: string; // Optional field for HttpUrl, which is just a string in TypeScript
  node_id: string;
}


export interface GitHubUser {
  login: string;
  id: number;
  node_id: string;
  avatar_url: string; // HttpUrl is represented as string in TypeScript
  gravatar_id?: string; // Optional field, empty by default
  url: string;
  html_url: string;
  followers_url: string;
  following_url: string;
  gists_url: string;
  starred_url: string;
  subscriptions_url: string;
  organizations_url: string;
  repos_url: string;
  events_url: string;
  received_events_url: string;
  type: string;
  site_admin: boolean;
  score?: number; // Optional float
}


export interface GitHubRepository {
  id: number;
  node_id: string;
  name: string;
  full_name: string;
  private: boolean;
  owner: GitHubUser;
  html_url: string;
  description?: string; // Optional string
  fork: boolean;
  url: string;
  forks_url: string;
  keys_url: string;
  collaborators_url: string;
  teams_url: string;
  hooks_url: string;
  issue_events_url: string;
  events_url: string;
  assignees_url: string;
  branches_url: string;
  tags_url: string;
  blobs_url: string;
  git_tags_url: string;
  git_refs_url: string;
  trees_url: string;
  statuses_url: string;
  languages_url: string;
  stargazers_url: string;
  contributors_url: string;
  subscribers_url: string;
  subscription_url: string;
  commits_url: string;
  git_commits_url: string;
  comments_url: string;
  issue_comment_url: string;
  contents_url: string;
  compare_url: string;
  merges_url: string;
  archive_url: string;
  downloads_url: string;
  issues_url: string;
  pulls_url: string;
  milestones_url: string;
  notifications_url: string;
  labels_url: string;
  releases_url: string;
  deployments_url: string;
  created_at: Date;
  updated_at: Date;
  pushed_at?: Date; // Optional datetime
  git_url: string;
  ssh_url: string;
  clone_url: string;
  svn_url: string;
  homepage?: string; // Optional HttpUrl or string
  size: number;
  stargazers_count: number;
  watchers_count: number;
  language?: string; // Optional string
  has_issues: boolean;
  has_projects: boolean;
  has_downloads: boolean;
  has_wiki: boolean;
  has_pages: boolean;
  has_discussions: boolean;
  forks_count: number;
  mirror_url?: string; // Optional HttpUrl
  archived: boolean;
  disabled: boolean;
  open_issues_count: number;
  license?: GitHubLicense; // Optional License object
  allow_forking: boolean;
  is_template: boolean;
  web_commit_signoff_required: boolean;
  topics?: string[]; // Optional list of strings
  visibility: string;
  forks: number;
  open_issues: number;
  watchers: number;
  default_branch: string;
  score: number;
}


export interface GitHubSearchResult {
  results?: (GitHubUser | GitHubRepository)[];
  search_params?: GitHubSearchParams;
}


const searchTypeMap: { [key: string]: SearchType } = {
  user: SearchType.USER,
  repo: SearchType.REPO,
  issue: SearchType.ISSUE,
}


export const getSearchType = (type_value: string) => {
  type_value = type_value.toLowerCase();
  return searchTypeMap[type_value] ?? SearchType.USER;
}
