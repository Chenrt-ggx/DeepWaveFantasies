# 深邃幻想，但不黑暗

![license](https://img.shields.io/github/license/Chenrt-ggx/DeepWaveFantasies)

> Do You Like ♂ What You See?

## 使用方法

- 在 `auth.json` 设置账号密码。
- 使用 `python wifi.py login` 单次登录，可配置重试次数。
- 使用 `python wifi.py test` 测试连接情况，方式是请求 `https://www.baidu.com`。
- 使用 `python wifi.py keep` 保持登录，方式是隔一段时间检测一次是否连接，未连接就登录，可配置时间间隔。

## 配置选项

- `request` 字段中的 `ua` 字段可考虑修改，此外 `jquery` 字段曾经暗改过，感觉不会很频繁的改就写在配置里面了，其它字段应该不用改。
- `encrypt` 字段是魔改 `base64` 加密用的，前端写死了且没暗改过，应该不用改。
- `misc` 字段中的 `os` 和 `name` 字段可考虑修改，其它字段意义不明且没暗改过，应该不用改。
- `proxies` 字段为代理配置，当其中的 `enable` 字段为真时非前端资源的请求走代理。
- `run` 字段为运行时配置，其中 `retry` 字段为尝试链接次数，`interval` 字段为保持连接时的检测间隔。

## 反检测特性

- 额外请求前端资源，请求附带 Cookies。
- 时间戳延迟随机化，请求等待时间随机化。
