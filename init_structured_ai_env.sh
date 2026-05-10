#!/usr/bin/env bash

# 这个脚本设计为被 `source` 调用，因此不要在这里修改调用方 shell 的
# `set -e/-u/-o pipefail` 行为，否则后续命令出错时可能直接把当前终端退出。

_structured_ai_env_fail() {
  echo "[init_structured_ai_env] $1" >&2
  return 1 2>/dev/null || exit 1
}

# 基于当前仓库在本机的位置初始化结构化 AI 服务的 SSH 通信环境变量。
# 使用方式：
#   source /home/cirmatic/BUAA/SE/BUAASE_2026/init_structured_ai_env.sh
#
# 说明：
# 1. 默认按“本机即远端”配置，后端会通过 SSH 连接 127.0.0.1。
# 2. 优先使用 SSH key 登录；如果你本机 SSH 只开了密码登录，请自行 export STRUCTURED_AI_PASSWORD。
# 3. 启动 AI 服务前，请先确保本机 sshd 已启动，且下面的 Python 路径可用。

PROJECT_ROOT="/home/cirmatic/BUAA/SE/BUAASE_2026"
AI_SERVICE_ROOT="${PROJECT_ROOT}/AI学术鉴伪/代码/AI服务/AI服务器代码"
STRUCTURED_REQUEST_DIR="${AI_SERVICE_ROOT}/structured_test"

mkdir -p "${STRUCTURED_REQUEST_DIR}" || _structured_ai_env_fail "无法创建目录: ${STRUCTURED_REQUEST_DIR}"

LOCAL_USER="${USER:-$(whoami)}"

# 你也可以在 source 之前手动 export STRUCTURED_AI_PYTHON 覆盖它。
if command -v python3 >/dev/null 2>&1; then
  STRUCTURED_AI_PYTHON_DEFAULT="python3"
else
  STRUCTURED_AI_PYTHON_DEFAULT="python"
fi
STRUCTURED_AI_PYTHON="${STRUCTURED_AI_PYTHON:-$STRUCTURED_AI_PYTHON_DEFAULT}"

command -v "${STRUCTURED_AI_PYTHON}" >/dev/null 2>&1 || _structured_ai_env_fail "找不到 Python 可执行文件: ${STRUCTURED_AI_PYTHON}"

export STRUCTURED_AI_REMOTE_ROOT="${AI_SERVICE_ROOT}"
export STRUCTURED_AI_REMOTE_REQUEST_DIR="${STRUCTURED_REQUEST_DIR}/"
export STRUCTURED_AI_REMOTE_COMMAND="cd \"${AI_SERVICE_ROOT}\" && \"${STRUCTURED_AI_PYTHON}\" trigger_structured.py"

export STRUCTURED_AI_HOST="${STRUCTURED_AI_HOST:-127.0.0.1}"
export STRUCTURED_AI_PORT="${STRUCTURED_AI_PORT:-22}"
export STRUCTURED_AI_USERNAME="${STRUCTURED_AI_USERNAME:-$LOCAL_USER}"

# 如果你配置了本机 SSH key 免密登录，可以保持为空。
# 如果需要密码登录，请在 source 之后执行：
#   export STRUCTURED_AI_PASSWORD='你的SSH密码'
export STRUCTURED_AI_PASSWORD="${STRUCTURED_AI_PASSWORD:-}"

export STRUCTURED_AI_READY_MARKER="${STRUCTURED_AI_READY_MARKER:-structured ready}"
export STRUCTURED_AI_RESULT_MARKER="${STRUCTURED_AI_RESULT_MARKER:-structured results}"
export STRUCTURED_AI_CONNECT_TIMEOUT="${STRUCTURED_AI_CONNECT_TIMEOUT:-10}"
export STRUCTURED_AI_READY_TIMEOUT="${STRUCTURED_AI_READY_TIMEOUT:-60}"
export STRUCTURED_AI_RESULT_TIMEOUT="${STRUCTURED_AI_RESULT_TIMEOUT:-120}"
export STRUCTURED_AI_SUBMIT_RETRY="${STRUCTURED_AI_SUBMIT_RETRY:-2}"

# 结构化 AI 模型目录。没有训练产物时，trigger_structured.py 会退化到启发式/无监督逻辑。
export STRUCTURED_AI_MODEL_DIR="${STRUCTURED_AI_MODEL_DIR:-${AI_SERVICE_ROOT}/structured_models}"
export STRUCTURED_AI_ENABLE_ML="${STRUCTURED_AI_ENABLE_ML:-1}"

cat <<EOF
Structured AI env initialized.

PROJECT_ROOT=${PROJECT_ROOT}
AI_SERVICE_ROOT=${AI_SERVICE_ROOT}
STRUCTURED_AI_HOST=${STRUCTURED_AI_HOST}
STRUCTURED_AI_PORT=${STRUCTURED_AI_PORT}
STRUCTURED_AI_USERNAME=${STRUCTURED_AI_USERNAME}
STRUCTURED_AI_REMOTE_REQUEST_DIR=${STRUCTURED_AI_REMOTE_REQUEST_DIR}
STRUCTURED_AI_REMOTE_COMMAND=${STRUCTURED_AI_REMOTE_COMMAND}
STRUCTURED_AI_MODEL_DIR=${STRUCTURED_AI_MODEL_DIR}

Next steps:
1. 确保本机 sshd 已启动，并且 ${STRUCTURED_AI_USERNAME}@${STRUCTURED_AI_HOST} 可登录。
2. 如需密码登录，补充：
   export STRUCTURED_AI_PASSWORD='你的SSH密码'
3. 启动后端与 celery。
EOF
