import requests
import os,json
import json
from dotenv import load_dotenv
load_dotenv()

# 使用对方给你的新令牌 需要本地获取
token = os.environ.get('github_token')

print(token)
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
}

# 获取用户的所有仓库
def get_repositories():
    url = "https://api.github.com/user/repos"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve repositories: {response.status_code}")
        print(response.json())
        return []

def get_all_repos_contributors(repos):
    base_url = "https://api.github.com"
   
    repos_info = []
    
    for repo in repos:
        repo_owner=repo['owner']['login']
        repo_name = repo['name']
        contributors_url = f"{base_url}/repos/{repo_owner}/{repo_name}/contributors"
        contributors_response = requests.get(contributors_url,headers=headers)
        contributors = contributors_response.json()
        
        contributor_names = [contributor['login'] for contributor in contributors]
        
        repos_info.append({
            "repo_name": repo_name,
            "contributors": contributor_names
        })
    return repos_info


def get_one_repo_contributors(repo_owner, repo_name):

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contributors"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        contributors = response.json()
        return [{"repo_owner": contributor["login"], "contributions": contributor["contributions"]} for contributor in contributors]
    else:
        print("无法获取贡献者信息，状态码：", response.status_code)
        return []

def save_info_to_json(info_dict, filename):

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(info_dict, f, ensure_ascii=False, indent=4)


def get_all_issues_and_prs(repo_owner, repo_name):
    base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    
    
    # 获取 issues
    issues_url = f"{base_url}/issues"
    issues_response = requests.get(issues_url, headers=headers)
    issues = issues_response.json() if issues_response.status_code == 200 else []
    
    # 获取 pull requests
    prs_url = f"{base_url}/pulls"
    prs_response = requests.get(prs_url, headers=headers)
    prs = prs_response.json() if prs_response.status_code == 200 else []
    
    return issues, prs

if __name__ == "__main__":



    #获取所有仓库信息
    repos = get_repositories()
    # save_info_to_json(repos, "./github_data/all_repos.json")

    
    all_issues = []
    all_prs = []

    # 获取每个仓库的所有issues和PRs
    # for repo in repos:
    #     repo_owner = repo['owner']['login']
    #     repo_name = repo['name']
    #     print(f'repo_name {repo_name}')
    #     issues, prs = get_all_issues_and_prs(repo_owner, repo_name)
    #     issue_html = [issue['html_url']for issue in issues]
    #     print(f'issue_html {issue_html}')

    #     issues_closed = [issue for issue in issues if 'issues' in issue['html_url'] and issue['state']=='closed']
    #     issues_open = [issue for issue in issues if 'issues' in issue['html_url'] and issue['state']=='open']

    #     for item in [issues_closed,issues_open]:
    #         if item:
    #             state = item[0]['state']
    #             filename = f'./github_data/{repo_name}_issue_{state}.json'
    #             with open(filename, 'w', encoding='utf-8') as f:
    #                 json.dump(item, f, ensure_ascii=False, indent=4)


    #     pr_closed = [pr for pr in prs if 'pull' in pr['html_url'] and pr['state']=='closed']
    #     pr_open = [pr for pr in prs if 'pull' in pr['html_url'] and pr['state']=='open']
    #     for item in [pr_closed,pr_open]:
    #         if item:
    #             state = item[0]['state']
    #             filename = f'./github_data/{repo_name}_pr_{state}.json'
    #             with open(filename, 'w', encoding='utf-8') as f:
    #                 json.dump(item, f, ensure_ascii=False, indent=4)


    # #获取所有仓库贡献者
    repos_info = get_all_repos_contributors(repos)
    print(repos_info)

    save_info_to_json(repos_info, "./github_data/all_repos_contributors.json")

    # 获取单个仓库贡献者
    # repo_name = 'Hackathon'
    # contributors = get_one_repo_contributors(repo_owner, repo_name)
    # print(contributors)
    # save_info_to_json(contributors, f'{repo_name}_contributors.json')

