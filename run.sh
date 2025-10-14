# 1. Initialize Git LFS
git lfs install

# 2. Track all files above 100 MB automatically
# (This finds large files and tracks them with LFS)
find . -type f -size +100M -exec git lfs track "{}" \;

# 3. Add the .gitattributes file created by Git LFS
git add .gitattributes

# 4. Add all files (including large ones)
git add .

# 5. Commit everything
git commit -m "Add all files using Git LFS"

# 6. Push to GitHub (replace main with your branch if needed)
git push origin main
