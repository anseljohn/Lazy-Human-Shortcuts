mkdir ~/.lhs
mkdir ~/.lhs/scripts
mkdir ~/.lhs/embeddings
touch ~/.lhs/aliases.zsh
touch ~/.lhs/manifest.json

echo "{}" > ~/.lhs/manifest.json

pip install e .