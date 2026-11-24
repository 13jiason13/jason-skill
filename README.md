# Jason Skill

为 Codex 打包的文件、浏览器和桌面操作流程。使用同一安装文件配置 macOS 或 Windows，按任务验证输入、提交、保存与文件内容。

- [下载单文件安装器](Jason-Skill-0.2.2-install.txt) · [下载完整 MIT 源码 ZIP](Jason-Skill-0.2.2-source.zip) · [校验 SHA-256](SHA256SUMS.txt)
- [版本说明](RELEASE-NOTES.md) · [隐私与安全](SECURITY.md) · [MIT 许可证](LICENSE)

## 安装

先核对下载校验值。将安装 TXT 拖入能访问本机文件和终端的 Codex，对它说「安装 Jason Skill，并配置我需要的桌面和网页工具」。安装器使用 Python 3.8+。Windows 可以使用 `py -3`。安装后调用 `$jason-skill`。第三方依赖走各自官方源，系统权限由使用者在本机授予。

## 能力

| 功能 | 主要工具 | 验收 |
| --- | --- | --- |
| 文件读写、整理与批处理 | Codex 文件工具、终端 | 对照实际文件路径和内容 |
| 网页浏览、填写、提交 | 隔离浏览器或 agent-browser | 验证页面实际结果 |
| 窗口读取、按钮、输字、勾选、保存 | Computer Use、agent-desktop 或可选 Cua Driver | 读回应用状态并验证保存文件 |

完整 ZIP 含安装源码、依赖选择、跨平台测试窗口、基准说明、安装指南和去标识测试数据。27 项本地自动测试通过。Windows 依赖选择已做模拟，Windows GUI、特定应用和速度仍需真机验收。Windows ARM64 的 agent-browser 可在 Windows 11 尝试 x64 仿真。

源码和配套脚本采用 MIT 许可证。公开文件不包括发布者的账户信息、凭据、浏览器数据或系统授权。
