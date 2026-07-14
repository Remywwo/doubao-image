# doubao-image

Doubao Image 是一个 Dify 工具插件，通过火山方舟 Ark 调用豆包生成模型，根据文本提示词生成图片或视频。

## 功能

- 使用豆包 Seedream 模型生成图片。
- 使用豆包 Seedance 模型生成视频。
- 图片结果可返回 URL 或二进制图片输出。
- 视频生成会轮询任务状态，并返回最终视频 URL。

## 使用要求

- 已启用插件能力的 Dify Community Edition 或 Dify Cloud。
- 拥有可访问所选豆包生成模型的火山方舟账号。
- 火山方舟 API Key。
- Dify 插件运行环境需要能访问 `https://ark.cn-beijing.volces.com`。

## 配置步骤

1. 在 Dify 中安装插件。
2. 打开插件供应商配置。
3. 在 `API Key` 中填写火山方舟 API Key。
4. 选择默认豆包模型 ID，也可以在每次工具调用时覆盖该模型。
5. 保存配置。

## 使用方式

在 Dify workflow、chatflow 或 agent 中使用 `Generate Image or Video` 工具。

必填参数：

- `prompt`：用于生成图片或视频的文本提示词。

可选参数：

- `model`：豆包模型 ID。Seedream 模型生成图片，Seedance 模型生成视频。
- `response_format`：图片返回格式，可选 `url` 或 `b64_json`。
- `ratio`：视频画面比例，仅视频模型使用。
- `duration`：视频时长，单位秒，仅视频模型使用。

## 凭证和数据流

插件会将提示词、模型 ID 和生成参数发送到火山方舟 API。API Key 由 Dify 作为密钥凭证保存，仅用于认证火山方舟请求。

插件不会存储提示词、API Key、生成媒体或用户数据。

## 测试状态和限制

当前仓库已完成 Dify Marketplace 提交要求相关的静态检查和 Python 语法检查。

Dify Community Edition 和 Dify Cloud 的端到端运行验证需要有效的火山方舟 API Key，以及所选豆包模型的访问权限。如果提交 Marketplace 前未覆盖任一平台测试，请在 PR checklist 中说明该限制。

## 风险说明

本插件会将用户提示词和生成参数发送到固定的第三方 HTTPS API 端点：火山方舟。插件不会执行用户代码、运行 shell 命令、访问本地文件，也不会代理任意 URL。

## 源码

源码仓库：https://github.com/Remywwo/doubao-image
