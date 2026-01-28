I cannot directly delete a repository from your GitHub account as I do not have those permissions. You must perform the deletion manually on the GitHub website. However, I can help you reset your local configuration to point to a new repository.

# Repository Reset Plan

## 1. Delete Remote Repository (User Task)
You need to delete the repository on GitHub:
1. Go to your repository settings: [https://github.com/TheReaLsshhh/ccbwebmain/settings](https://github.com/TheReaLsshhh/ccbwebmain/settings)
2. Scroll to the bottom "Danger Zone".
3. Click **Delete this repository**.
4. Follow the confirmation prompts.

## 2. Create New Repository (User Task)
1. Create your new repository on GitHub (with the same name or a new one).
2. **Copy the new HTTPS URL** (e.g., `https://github.com/TheReaLsshhh/new-repo-name.git`).

## 3. Local Git Reset (My Task)
Once you provide the new URL, I will:
1. Remove the old remote link: `git remote remove origin`
2. Add the new remote link: `git remote add origin <NEW_URL>`
3. Push the current code to the new repository.

**Please delete the repository, create the new one, and then paste the new repository URL here so I can proceed.**