# website

基于 Vue 3 + Vite 的前端项目。

## 技术栈

- [Vue 3](https://vuejs.org/)（`<script setup>` 单文件组件）
- [Vite](https://vite.dev/) 构建与开发服务器

## 环境要求

- Node.js ^20.19.0 或 >=22.12.0
- npm（或 pnpm / yarn）

## 快速开始

```bash
# 安装依赖
npm install

# 启动开发服务器（默认 http://localhost:5173）
npm run dev

# 生产构建，产物输出到 dist/
npm run build

# 本地预览生产构建产物
npm run preview
```

## Docker 部署

镜像采用多阶段构建：先在 Node 环境中执行 `npm ci && npm run build`，再由 Nginx 托管 `dist/` 静态产物（已配置单页应用回退、gzip 压缩与静态资源长效缓存）。

```bash
# 构建镜像
docker build -t website .

# 启动容器，映射到本机 8080 端口
docker run -d --name website -p 8080:80 website

# 停止并移除容器
docker stop website && docker rm website
```

启动后访问 http://localhost:8080 即可。如需修改端口映射、缓存策略或 gzip 规则，编辑 [nginx.conf](nginx.conf) 后重新构建镜像。

## 部署到 Cloudflare Workers

以 Workers 静态资源（Static Assets）方式托管：`vite build` 产物目录 `dist/` 直接作为 assets 上传，无需编写 Worker 脚本，配置见 [wrangler.jsonc](wrangler.jsonc)。

- `not_found_handling: "single-page-application"`：未命中静态文件时回退到 `index.html`，等价于 Nginx 的 `try_files` 回退
- [public/_headers](public/_headers)：为哈希产物设置长期缓存，HTML 入口每次回源校验

```bash
# 首次使用需登录 Cloudflare 账号（浏览器授权）
npx wrangler login

# 本地预演：构建后用 Wrangler 本地运行时提供站点
npm run cf:dev

# 构建并部署
npm run deploy
```

部署完成后会输出访问地址（默认为 `https://website.<你的子域>.workers.dev`）。如需绑定自定义域名，在 Cloudflare 控制台的 Workers 项目中添加 Custom Domain 即可。

## 目录结构

```
website/
├─ public/              # 静态资源，原样拷贝到构建产物根目录（含 _headers 缓存规则）
├─ src/
│  ├─ assets/           # 需要被构建处理的资源（图片、样式等）
│  ├─ components/       # 通用组件
│  ├─ App.vue           # 根组件
│  ├─ main.js           # 应用入口，挂载 Vue 实例
│  └─ style.css         # 全局样式
├─ index.html           # HTML 入口
├─ vite.config.js       # Vite 配置
├─ Dockerfile           # 多阶段构建：Node 构建 + Nginx 托管
├─ nginx.conf           # Nginx 站点配置（SPA 回退、gzip、静态资源缓存）
├─ wrangler.jsonc       # Cloudflare Workers 部署配置（静态资源 + SPA 回退）
├─ .dockerignore        # 构建镜像时忽略的文件
└─ package.json
```

## 开发说明

- 组件统一使用 `<script setup>` 语法；单文件组件（SFC）说明见 [Vue 官方文档](https://vuejs.org/guide/scaling-up/sfc.html)。
- 需要 Vite 处理的资源放在 `src/assets/` 并用 `import` 引入；无需处理的静态资源放在 `public/`。
- 使用 VS Code 开发时，建议安装 [Vue - Official](https://marketplace.visualstudio.com/items?itemName=Vue.volar) 扩展，以获得语法高亮、类型提示与模板智能补全。