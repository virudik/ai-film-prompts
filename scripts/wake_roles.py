"""Shared site/video executor roles. No network, settings writes or launch authority."""

ACTORS = frozenset(("dot", "grok"))
RUNNER_ACTORS = {
    "chatgpt_event_trigger": "dot",
    "dot_event_handler": "dot",
    "chatgpt_interactive_delegated": "dot",
    "grok_event_handler": "grok",
    "grok_scheduled_routine": "grok",
}


def resolve(config):
    """Absent block preserves legacy order; an explicit invalid block fails closed."""
    if not isinstance(config, dict):
        return None
    if "wake_roles" not in config:
        return {"primary_actor": "dot", "backup_actor": "grok", "explicit": False}
    block = config["wake_roles"]
    if not isinstance(block, dict):
        return None
    primary, backup = block.get("primary_actor"), block.get("backup_actor")
    if (not isinstance(primary, str) or not isinstance(backup, str) or
            primary not in ACTORS or backup not in ACTORS or primary == backup):
        return None
    return {"primary_actor": primary, "backup_actor": backup, "explicit": True}


def actor_for(config, role):
    roles = resolve(config)
    return roles.get(role + "_actor") if roles and role in ("primary", "backup") else None


def receipt_actor(receipt):
    """Explicit actor wins; only known exact old runner names are migration aliases."""
    if not isinstance(receipt, dict):
        return None
    if "actor" in receipt:
        value = receipt["actor"]
        return value if isinstance(value, str) and value in ACTORS else None
    return RUNNER_ACTORS.get(receipt.get("runner")) if isinstance(receipt.get("runner"), str) else None
