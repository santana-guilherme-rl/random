# V1 doesn't use gh. Its only idea is to make the branch creation faster

# 0º script name....
# 1º Commit hash
# 2º List of target branches separated by comma
# 3º Branch name
# ex: hotfix-it <commit-hash> release/2025.0401,release/2025.0421 RD-12345

# save the current state we are in
stash_random_string=$(openssl rand -base64 16)
original_branch=$(git rev-parse --abbrev-ref HEAD)
stash_message="hotfix-it stash: $stash_random_string ($original_branch)"
git stash push -m "$stash_message"

# we probably need to change branches and make a pull -r on master
git checkout master && git pull -r
# make sure the commit hash exists
git show $1 -q &> /dev/null
if [[ $? != 0 ]]; then
    echo "the commit hash doesn't exists on master"
    exit 128
fi
# make sure the list of target branches exists
IFS=',' read -ra branches <<< "$2"

origin_branches=$(git branch -r)
for branch_name in "${branches[@]}"; do
    exists=$(echo $origin_branches | grep $branch_name)
    if [[ ${#exists} -lt 1 ]]; then
        echo "the target branch '$branch_name' doesn't exist"
        exit 128
    fi
done
# create the branch with specific name (optionally get from command line) hotfix/<BRANCH-NAME>_<SOMETHING FROM THE TARGET BRANCH>
for branch_name in "${branches[@]}"; do
    git checkout $branch_name && git pull -r > /dev/null
    new_hotfix_branch="hotfix/$3_${branch_name: -4}"
    git checkout -b $new_hotfix_branch > /dev/null
    # print the branch name
    echo "New branch $new_hotfix_branch created"
    # cherry-pick the commit to this new branch
    git cherry-pick $1 > /dev/null
    # push the branch
    git commit
    git push -u origin $new_hotfix_branch > /dev/null
done

# retore the previous state we were
git checkout $original_branch > /dev/null

# TODO: TEST THIS
# check if the last stash is the one we added
git stash list | head -n 1 | grep "$stash_message"
if [[ $? == 0 ]]; then
    echo "restoring last stash to the current branch"
    git stash pop > /dev/null
else
    echo "nothing to restore from stash"
fi

exit 0
#while getopts "ctb"
