#!/bin/sh

# Set up pre-push hook to run lint and tests
cat << 'EOF' > .git/hooks/pre-push
#!/bin/sh
poetry run lint || exit 1
poetry run test || exit 1
echo "Pre-push checks passed."
EOF
chmod +x .git/hooks/pre-push

# Set commit message template
if [ -f .gitmessage ]; then
  git config commit.template .gitmessage
fi

direnv allow