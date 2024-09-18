export const enum SearchType {
  USER = "user",
  REPO = "repo",
  ISSUE = "issue",
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
