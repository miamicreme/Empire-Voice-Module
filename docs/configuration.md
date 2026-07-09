# Configuration Best Practices

Empire Voice configuration should be explicit, validated, portable, and safe.

## Config Sources

Use this priority order:

1. built-in safe defaults,
2. setup wizard output,
3. local user config file,
4. environment overrides for development only.

Do not require users to hand-edit JSON for normal setup.

## Recommended Config Path

```text
~/.config/empire-voice/config.json
```

On Windows, use the platform equivalent app config directory.

## Config Categories

| Category | Examples |
|---|---|
| Assistant | name, wake phrase, follow-up window |
| Audio | mic device, output device, noise gate |
| STT | backend, model, language |
| TTS | enabled, voice, speed |
| Privacy | memory policy, redaction, log retention |
| Modules | enabled targets and local endpoints |
| MCP | servers, permissions, disabled tools |
| UI | tray, notifications, theme |
| Evals | test mode, sample commands |

## Secret Handling

Do not store secrets in plain config.

Use:

- OS keychain,
- encrypted local store,
- environment variable reference,
- prompt at runtime.

Config may store a reference:

```json
{
  "api_key_ref": "keychain:worldmonitor_api_key"
}
```

It should not store:

```json
{
  "api_key": "actual-secret-value"
}
```

## Validation Rules

Startup should fail gracefully when:

- config is missing required fields,
- selected microphone is unavailable,
- selected model is unavailable,
- module endpoint is invalid,
- MCP server config is malformed,
- risky permissions are set to always allow.

## Migration Rule

Config must include a version:

```json
{
  "config_version": "0.1.0"
}
```

When breaking fields change, add migration logic rather than silently ignoring old config.
