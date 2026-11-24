# 发布包的安全与隐私

- Jason Skill 的安装文件是可读文本。仅分发本项目 Skill、可审查安装源码、合成测试窗口、去标识计时和许可证。包内 SHA-256 用于完整性检查；请从可信的 Release 核对**整个文件**的 SHA-256 后再运行。
- 安装基础 Skill 可以离线完成。依赖预览不下载。实际依赖配置需明确使用 `--apply`，从对应官方 Release 下载，校验固定 SHA-256 和版本。Mac Cua App 此外校验 Apple 签名、开发者 Team ID 和 Gatekeeper。Windows Cua 固定哈希并检查程序版本；Windows 安全策略阻止运行时，保留系统保护并记录跳过。补装浏览器运行时需额外使用 `--browser-runtime`，该动作会运行上游自己的下载程序。
- 不分发发布者的账号、浏览器资料、SSH 密钥、远程连接信息、真实操作录像或系统授权。脚本不修改 TCC、全局 MCP、全局 PATH、系统代理或网络设置。
- 自动化进程、网页和桌面诊断可能接触敏感数据。用任务专用会话和自建测试资料，不公开原始快照、录屏、终端日志或剪贴板内容。权限由电脑所有者授予。
- 第三方程序执行各自的隐私机制。生成的 Cua MCP 片段要求子进程退出遥测；若使用独立运行的 Cua daemon，按上游设置检查其有效状态。公开包不承诺关闭宿主或其他第三方服务的遥测。
- 开源发布只对这里的 Jason Skill 源码适用 MIT。第三方二进制由上游分发。若发现凭据或私人资料已外泄，应先撤销凭据，再按 GitHub 指引清理历史。向维护者报告时使用私密渠道和去标识复现，避免在公开 Issue 中粘贴敏感数据。

上游与平台参考：[Cua 遥测源代码](https://github.com/trycua/cua/tree/cua-driver-rs-v0.55.0/libs/cua/crates/cua-telemetry)、[GitHub 推送保护](https://docs.github.com/en/code-security/concepts/secret-security/push-protection)、[GitHub 使用政策](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies)。
