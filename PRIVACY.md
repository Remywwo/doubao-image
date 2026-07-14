# Privacy Policy

Doubao Image is a Dify tool plugin that sends user-provided prompts and generation options to the Volcengine Ark API in order to generate images or videos with Doubao models.

## Data Collected by the Plugin

The plugin does not collect, persist, or independently log user data.

During a tool call, the plugin processes:

- The text prompt provided by the user or workflow.
- The selected Doubao model ID.
- Image or video generation options such as response format, aspect ratio, and duration.
- The Volcengine Ark API key configured as a Dify secret provider credential.

## Data Sent to Third Parties

The plugin sends the prompt, model ID, and generation options to Volcengine Ark at `https://ark.cn-beijing.volces.com`.

The API key is sent only as an authorization credential for Volcengine Ark API requests.

## Data Storage

The plugin does not store prompts, API keys, generated media, or API responses.

Dify stores provider credentials according to Dify's own credential handling and secret storage behavior.

## Logs

The plugin does not intentionally log prompts, API keys, generated media, or API responses.

## Generated Content

Generated image or video URLs and structured metadata returned by Volcengine Ark are passed back to Dify as tool output. Any retention of those outputs is controlled by the user's Dify deployment and workflow configuration.

## Contact

For source code and issue reporting, use the source repository:

https://github.com/Remywwo/doubao-image
