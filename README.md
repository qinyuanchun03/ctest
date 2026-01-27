# Cloudflare 优选域名监控系统

这是一个基于 GitHub Actions 的轻量级监控工具，用于周期性检测 Cloudflare 优选域名的延迟与连通性。

## 当前状态

| 域名 | 电信 | 联通 | 移动 | 状态 |
|---|---|---|---|---|
| 等待首次运行... | - | - | - | ⚪ |

*结果每 30 分钟自动更新一次。*

## 工作原理
1.  **调度器**: GitHub Actions (`.github/workflows/monitor.yml`) 每 30 分钟触发一次。
2.  **探针**: `src/monitor.py` 读取 `data/domains.txt` 中的域名列表。
3.  **检测**: 模拟（或实际）检测域名在三网（电信、联通、移动）下的延迟数据。
4.  **报告**: 自动更新本文件 (`README.md`) 的状态表格，并记录历史数据到 `data/history.json`。

## 如何配置
- **修改域名**: 编辑 `data/domains.txt` 文件，每行一个域名。
- **配置探针**: 修改 `src/probe.py` 以对接真实的拨测 API（如 ITDog, Boce 等）。

## 部署说明
详细部署步骤请参考 [使用指南](walkthrough.md)。
