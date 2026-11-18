"""Pure provenance builder for new launcher receipts; never submits or writes files.

Capture started_at at actual runtime entry, before scan/lease acquisition. Pass only
observed trigger metadata; automation_id or actor.kind alone cannot distinguish
scheduled, manual run_now and webhook invocations. Historical receipts are untouched.
"""
from datetime import datetime
from uuid import UUID

TRIGGERS = {'scheduled', 'manual_run_now', 'webhook', 'interactive', 'not_exposed'}


def _time(value):
    try:
        dt = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
        if dt.tzinfo is not None:
            return dt
    except (ValueError, TypeError):
        pass
    raise ValueError('actual_timezone_aware_timestamp_required')


def build(*, execution_instance_id, actual_trigger, started_at, updated_at,
          automation_id=None, run_id=None, run_id_unavailable_reason=None,
          scan_checked_at=None, lease_acquired_at=None, completed_at=None):
    if str(UUID(execution_instance_id)) != execution_instance_id:
        raise ValueError('execution_uuid_required')
    if actual_trigger not in TRIGGERS:
        raise ValueError('observed_trigger_required')
    if actual_trigger in {'scheduled', 'manual_run_now', 'webhook'} and not automation_id:
        raise ValueError('automation_id_required')
    if run_id is not None and (not isinstance(run_id, str) or not run_id.strip()):
        raise ValueError('nonempty_runtime_id_or_null_required')
    if run_id is None and (not isinstance(run_id_unavailable_reason, str) or not run_id_unavailable_reason.strip()):
        raise ValueError('runtime_id_absence_reason_required')
    start, update = _time(started_at), _time(updated_at)
    if update < start:
        raise ValueError('receipt_time_order')
    for stamp in (scan_checked_at, lease_acquired_at, completed_at):
        if stamp is not None and not start <= _time(stamp) <= update:
            raise ValueError('receipt_time_order')
    return {'execution_instance_id': execution_instance_id, 'actual_trigger': actual_trigger,
            'automation_id': automation_id, 'run_id': run_id,
            'run_id_unavailable_reason': run_id_unavailable_reason if run_id is None else None,
            'started_at': started_at, 'updated_at': updated_at,
            'scan_checked_at': scan_checked_at, 'lease_acquired_at': lease_acquired_at,
            'completed_at': completed_at}
