# 新增同步镜像指南

本文说明：当你想让 Dependabot 跟踪一个新的 Docker 镜像，并把它自动同步到阿里云镜像仓库时，需要做的全部步骤。

> 阅读本文前，建议先了解仓库当前架构（见文末「整体流程」一节）。

---

## 步骤总览

新增一个镜像（例如 `someorg/some-image:1.2.3`）一共要改 / 新建 4 个地方：

1. `dependabot/<dir>/docker-compose.yml` —— 让 Dependabot 跟踪版本
2. `.github/dependabot.yml` —— 注册 Dependabot 的更新条目
3. `.github/workflows/sync-<name>.yml` —— 同步该镜像的 workflow
4. `scripts/sync_workflow_versions.py` 的 `MAPPINGS` —— 映射「compose 文件 → workflow 文件」，用于自动同步版本

下面逐步展开。示例统一以 **`someorg/some-image`** 为新镜像、**初始版本 `1.2.3`** 为例。

---

## 步骤 1：新建 `dependabot/<dir>/docker-compose.yml`

每条镜像线必须有自己的独立目录（避免同一个 dependency-name 在同一个文件里多行造成 Dependabot 任务互相阻塞）。

> 命名建议：和 sync workflow 文件名对应，例如 `dependabot/some-image/docker-compose.yml` 对应 `sync-some-image.yml`。
> 如果同一个镜像需要按多个轨道（例如 `mysql` 的 `8.0`、`8.4`、`9`），就拆成多个目录：`mysql-8.0/`、`mysql-8.4/`、`mysql-9/`。

文件内容模板：

```yaml
services:
  sync_some_image:
    image: focker.ir/someorg/some-image:1.2.3
```

要点：

- `services` 下只放一个服务，service 名建议统一加 `sync_` 前缀，并把版本号里的 `.` 改成 `_`（不强制，但当前仓库都这么写）。
- `image` 一律使用 `focker.ir/<repo path>:<tag>` 写法（仓库统一从 `focker.ir` 拉源，避免 Docker Hub 限流）。
  - **官方库** 镜像（如 `nginx`、`mysql`、`redis`，没有 `/`）路径要加 `library/`，写成 `focker.ir/library/<image>:<tag>`。
  - **带命名空间** 的镜像（如 `drone/drone`、`vaultwarden/server`）保持原命名空间，写成 `focker.ir/<ns>/<image>:<tag>`。

---

## 步骤 2：在 `.github/dependabot.yml` 增加 updates 项

在 `updates:` 列表里追加一段：

```yaml
  - package-ecosystem: docker-compose
    directory: /dependabot/some-image
    schedule:
      interval: daily
    open-pull-requests-limit: 5
    labels:
      - dependencies
      - docker
    commit-message:
      prefix: "feat"
```

可选：如果**只允许 patch 更新**（仅修补版，不要 minor / major 升级，例如 `mysql` / `redis` / `nginx`）：

```yaml
    ignore:
      - dependency-name: "someorg/some-image"
        update-types:
          - "version-update:semver-minor"
          - "version-update:semver-major"
```

> `dependency-name` 写 Dependabot 在 PR 里识别到的「依赖名」。如果不确定，留意 Dependabot 第一次开 PR 时的 `Bumps` 字段。
> 官方库镜像（如 `mysql`、`nginx`、`redis`）的 `dependency-name` 一般是裸名 `mysql` 而不是 `library/mysql`。

放置顺序建议按字母分组，方便阅读（drone / gitea / mysql / nginx / redis / vaultwarden / woodpecker ...）。

---

## 步骤 3：新建 `.github/workflows/sync-<name>.yml`

复制现有同类型的 workflow 改即可。下面是「常规模板」：

```yaml
name: Sync Some Image

on:
  push:
    branches:
      - main
    paths:
      - '.github/workflows/sync-some-image.yml'
  workflow_dispatch:

concurrency:
  group: sync-some-image-${{ github.ref }}
  cancel-in-progress: true

jobs:
  sync:

    runs-on: ubuntu-latest

    strategy:
      max-parallel: 2
      matrix:
        version:
          - "1"
          - "1.2.3"

    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4.0.0

      - name: Login to Aliyun
        uses: docker/login-action@v4.1.0
        with:
          registry: ${{ secrets.ALI_DOCKER_REPO }}
          username: ${{ secrets.ALI_DOCKER_USER }}
          password: ${{ secrets.ALI_DOCKER_PASS }}

      - name: Copy someorg/some-image:${{ matrix.version }} (buildx imagetools)
        env:
          SRC: ${{ secrets.DOCKERHUB_MIRROR }}/someorg/some-image:${{ matrix.version }}
          DST: ${{ secrets.ALI_DOCKER_REPO }}/mirrors_hub/some_image:${{ matrix.version }}
        run: |
          SRC_DIGEST="$(docker buildx imagetools inspect "$SRC" | awk '/^Digest:/ {print $2; exit}')"
          DST_DIGEST="$(docker buildx imagetools inspect "$DST" 2>/dev/null | awk '/^Digest:/ {print $2; exit}' || true)"
          if [ -z "$SRC_DIGEST" ]; then
            echo "Failed to resolve source digest: $SRC"
            exit 1
          fi
          if [ -n "$DST_DIGEST" ] && [ "$SRC_DIGEST" = "$DST_DIGEST" ]; then
            echo "Digest unchanged ($SRC_DIGEST), skip sync."
            exit 0
          fi
          docker buildx imagetools create --tag "$DST" "$SRC"
```

需要替换的地方：

- `name`：workflow 显示名
- `paths` 里的 `sync-some-image.yml`：改成实际文件名
- `concurrency.group`：改成 `sync-<name>`
- `matrix.version`：列出你想同步的 tag（参见步骤 4 的 style 列表，决定写法）
- `name: Copy ...`：仅显示用，写清楚
- `SRC`：源镜像路径，**通常和 `dependabot/<dir>/docker-compose.yml` 里的 `image` 路径一致**（去掉 `focker.ir/` 由 secret 提供）
- `DST`：阿里云上的路径，命名风格是把命名空间替换成下划线（`drone/drone-runner-docker` → `drone_runner`）

> 如果是官方库镜像（`mysql`、`nginx`、`redis`），`SRC` 必须写成 `${{ secrets.DOCKERHUB_MIRROR }}/library/<name>:...`，否则 buildx imagetools 找不到。

---

## 步骤 4：在 `scripts/sync_workflow_versions.py` 加映射

打开脚本里的 `MAPPINGS` 字典，按规则添加一行。键 = `dependabot/<dir>` 的目录名，value 描述如何在 workflow 的 `matrix.version` 里执行替换。

可用 `style` 一览：

| style | 含义 | `matrix.version` 期望写法 | 适用场景 |
|-------|------|--------------------------|----------|
| `full_only` | 只保留一个完整版本 | `["1.2.3"]` | 只同步精确版本，不要别名 |
| `major_full` | 一个 major 别名 + 一个完整版本 | `["1", "1.2.3"]` | major 跨越升级时也允许（drone / gitea-gitea） |
| `minor_full` | 一个 minor 别名 + 一个完整版本 | `["1.28", "1.28.3"]` | 只在某个 minor 内升级（nginx 当前模式） |
| `track_minor_full` | 同一个 workflow 内有多个 minor 轨道，每条独立维护 | 见 `mysql` | 多个 minor 并存，按 `track` 隔离 |
| `track_major_minor_full` | 同一 workflow 多个 minor 轨道，且每个还自带 major 别名 | 见 `redis` | 同上但有 major 别名 |

具体添加示例：

```python
MAPPINGS = {
    # ...
    "some-image": {
        "workflow": ".github/workflows/sync-some-image.yml",
        "style": "major_full",
    },
    # 多 track 示例：
    # "some-image-2": {
    #     "workflow": ".github/workflows/sync-some-image.yml",
    #     "style": "track_minor_full",
    #     "track": "2.5",
    # },
}
```

> `track` 写成 **当前 workflow `matrix.version` 中真实出现的 minor 字符串**。例如 mysql workflow 里有 `"8.4"`、`"8.4.9"` 这两行，那么 `mysql-8.4` 的 `track` 就是 `"8.4"`。

> ⚠️ `track` 是**字面量匹配**，跨 minor 升级（如 `8.4.9 -> 8.5.0`）时脚本会按当前 `track` 把 workflow 内的 `"8.4"` 改成 `"8.5"`，但 `MAPPINGS` 里写死的 `track` 字符串**不会自动更新**，下一次再升级到 8.5.x 时会失败。
>
> 实操上：mysql/nginx/redis 已用 `dependabot.yml` 的 `ignore` 规则锁定 patch-only，不会跨 minor 触发，所以 `track` 长期稳定。如果你确实需要让某个目录允许 minor 升级，记得在 PR 合并前一并把脚本里的 `track` 也改了。

---

## 步骤 5：本地验证（可选但强烈推荐）

```bash
# 模拟 Dependabot 改动后跑一遍脚本
python scripts/sync_workflow_versions.py dependabot/some-image/docker-compose.yml

# 检查 workflow 是否正确改动
git diff -- .github/workflows/sync-some-image.yml
```

如果输出 `[NOCHANGE] ...`，说明 compose 里的 tag 已经和 workflow 对齐；如果 `[UPDATED] ...`，说明替换成功。

---

## 整体流程（理解原理）

```
┌────────────────────────────────────────────────────────────────────┐
│ Dependabot                                                         │
│ ─ 每天读取 dependabot/<dir>/docker-compose.yml                      │
│ ─ 发现新版本时开 PR：修改其中的 image: tag                           │
└────────────┬───────────────────────────────────────────────────────┘
             │  PR 合入 main
             ▼
┌────────────────────────────────────────────────────────────────────┐
│ Workflow: auto-sync-workflow-versions.yml                          │
│ ─ 触发条件：push main 且改了 dependabot/**/docker-compose.yml         │
│ ─ 调用 scripts/sync_workflow_versions.py                            │
│   把 sync-*.yml 的 matrix.version 同步成新的 tag                     │
│ ─ commit & push 修改后的 sync-*.yml                                  │
│ ─ gh workflow run 主动触发被改过的 sync-*.yml                         │
└────────────┬───────────────────────────────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────────────────────┐
│ Workflow: sync-<name>.yml                                          │
│ ─ matrix 遍历多个 tag                                                │
│ ─ 比较 SRC / DST 的 digest，相同则跳过                                │
│ ─ 不同时用 docker buildx imagetools create 把镜像复制到阿里云         │
└────────────────────────────────────────────────────────────────────┘
```

如果上述任何一环漏配（例如忘了在 `MAPPINGS` 加映射），会出现的现象：

- 没加 `MAPPINGS`：Dependabot PR 合入后，sync workflow 的 matrix.version **不会被更新**（auto-sync 输出 `[SKIP] no mapping for ...`）。
- 没加 sync workflow：版本号仍会被脚本尝试更新，会报 `Could not find ...`，job 失败。
- `dependabot.yml` 没注册 directory：Dependabot 不会跟踪该目录，永远不开 PR。

---

## 常见检查清单（提交前）

- [ ] `dependabot/<dir>/docker-compose.yml` 存在，`image` 用 `focker.ir/...` 前缀
- [ ] `.github/dependabot.yml` 增加了对应 directory 的 updates 项
- [ ] `.github/workflows/sync-<name>.yml` 存在，含 `workflow_dispatch:` 触发器
- [ ] `scripts/sync_workflow_versions.py` 的 `MAPPINGS` 含有该 dir 的映射
- [ ] 本地跑 `python scripts/sync_workflow_versions.py dependabot/<dir>/docker-compose.yml` 输出 `[NOCHANGE]`
- [ ] 阿里云的 `mirrors_hub/<image>` 命名空间已存在或允许自动创建
