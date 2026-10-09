# LineageOS ANIP Icons

适用于 LineageOS ANIP 模块的公开图标数据仓库。初始版本为 696 个独立图形、775 个应用规则，包含小黑盒与 HMS Core 的图像生成派生桌面轮廓。

## 文件

- `anip/index.json`：应用包名、名称、颜色、图形引用、原贡献者。
- `anip/icons/`：原始通知 PNG 和可编辑矢量 JSON。`layers` 保留原通知轮廓，`desktopPath`（如有）用于桌面；模块 0.1.15 起支持 `notificationPath` 通知专用轮廓。HMS Core 的桌面与通知均使用生成稿派生轮廓。
- `channel/stable.json`：稳定版发布标签、SHA256、文件长度、兼容协议。
- Releases 的 `icons.zip`：供手机同步的完整数据包。
- `output/imagegen/`：两张已发布重绘稿及原提示词；不是运行时代码。

## 发布图标更新

修改矢量或索引，提交到 `main`，然后在 Actions 中运行 **Publish icons**。工作流检查路径、引用、原 PNG 哈希和大小限制，构建并发布 `icons.zip`，最后更新稳定版清单。发布失败时稳定版地址保持上一版。

图标包压缩后必须小于 4 MiB，解压总量小于 16 MiB，单条目不超过 1 MiB。达到上限需要升级模块协议与资源加载器；发布脚本会拒绝超限。

模块 WebUI 点击“同步图标”即可下载并校验。失败时保留当前包，成功时保存上一版；重启手机应用。仓库不提供 APK、DEX、脚本或原生库供模块下载执行。

## 来源与许可

原图与包名规则来自 [BetterAndroid/android-notification-icon-project](https://github.com/BetterAndroid/android-notification-icon-project)，固定发布版本 `54b3c62`，Apache-2.0。上游压缩包 SHA256：`f4c1ab1dee927585483144c554405e39385e61be2bed1e5a2c841ed2ca76538f`。原贡献者保留在索引中。品牌名称与标志属于各自权利人。

桌面曲线由本地 Potracer 生成；小黑盒与 HMS Core 使用内置 image_gen 重绘后再转换为矢量，PNG 与提示词随仓库保存。这些图形是原标志的主题派生稿。Potracer 仅用于离线制作，其 GPL-2.0-or-later 许可见 `licenses/`。原图与图形数据继续保留 ANIP 来源及 Apache-2.0 许可。
