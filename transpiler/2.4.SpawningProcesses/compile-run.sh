
SCRIPT_PATH=$0
SCRIPT_DIR=$(dirname $SCRIPT_PATH)

# 1. Compile Eva MPP to JS:
python $SCRIPT_DIR/run.py &&

# 2. Run compiled code:
node $SCRIPT_DIR/out.js

# echo ""