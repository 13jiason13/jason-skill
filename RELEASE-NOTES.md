# Jason Skill v0.2.2

Jason Skill 把电脑操作拆成文件、网页和原生窗口三条路线，根据目标选择工具，用页面或保存结果确认完成。Mac 和 Windows 使用同一安装包、安装入口和验收项目。

- 文件、网页和桌面流程可复用。依赖助手按平台选定 agent-browser、agent-desktop 和可选 Cua，用固定 SHA-256 验证官方文件。
- Windows x64 和 ARM64 有原生桌面工具。Windows 11 ARM 的浏览器可尝试 x64 仿真，安装和网页能力须分别验收。
- 新增 Mac 与 Windows 对等测试窗口、文件验收和跨平台复测说明。
- 隐私检查覆盖公开文件清单与内嵌包。此版本提供 MIT 源码与可检查的单文件安装器。

本地自动测试覆盖安装逻辑和资产选择。历史 Intel Mac 数据和本机修补版 Cua 的 GUI 验收见测试记录。Windows 真机 GUI、硬件速度和特定第三方应用仍需分别验证。
