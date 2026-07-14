# doubao-image

Doubao Image is a Dify tool plugin for generating images and videos with ByteDance Doubao generation models through Volcengine Ark.

## Features

- Generate images from text prompts with Doubao Seedream models.
- Generate videos from text prompts with Doubao Seedance models.
- Return generated images as URLs or binary image output.
- Poll video generation tasks and return the final video URL.

## Requirements

- Dify Community Edition or Dify Cloud with plugin support enabled.
- A Volcengine Ark account with access to the selected Doubao generation models.
- A Volcengine Ark API key.
- Outbound HTTPS access from the Dify plugin runtime to `https://ark.cn-beijing.volces.com`.

## Setup

1. Install the plugin in Dify.
2. Open the plugin provider settings.
3. Enter your Volcengine Ark API key in `API Key`.
4. Select the default Doubao model ID. You can override the model for each tool call.
5. Save the provider settings.

## Usage

Use the `Generate Image or Video` tool in a Dify workflow, chatflow, or agent.

Required parameter:

- `prompt`: the text prompt used to generate the image or video.

Optional parameters:

- `model`: Doubao model ID. Seedream models generate images; Seedance models generate videos.
- `response_format`: image response format, either `url` or `b64_json`.
- `ratio`: video aspect ratio. Used only by video models.
- `duration`: video duration in seconds. Used only by video models.

Example image prompt:

```text
A clean product photo of a ceramic coffee cup on a wooden desk, soft natural light
```

Example video prompt:

```text
A cinematic shot of clouds moving over a mountain lake at sunrise
```

## Credentials and Data Flow

The plugin sends the prompt, selected model ID, and generation options to the Volcengine Ark API. The API key is stored by Dify as a secret provider credential and is used only to authenticate requests to Volcengine Ark.

Generated image or video URLs are returned by Volcengine Ark and surfaced in Dify tool output. The plugin does not store prompts, API keys, generated media, or user data.

## Testing Status

This repository has been checked for Dify Marketplace submission requirements and basic Python syntax.

End-to-end runtime validation on Dify Community Edition and Dify Cloud requires a valid Volcengine Ark API key and access to the selected Doubao models. If either platform is not tested before a Marketplace submission, disclose that limitation in the pull request checklist.

## Risk and Limitations

This plugin sends user prompts and generation options to a fixed third-party HTTPS API endpoint, Volcengine Ark. It does not execute user-provided code, run shell commands, access local files, or proxy arbitrary URLs.

## Source

Source repository: https://github.com/Remywwo/doubao-image

## Privacy

See [PRIVACY.md](PRIVACY.md).
