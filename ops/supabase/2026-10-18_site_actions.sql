-- Owner site panel, 18.10.2026 (owner approval in project thread 17.10 22:48 UTC):
-- launch-queue buttons and reference feedback. Additive only: old actions keep working.
alter table public.owner_decisions drop constraint owner_decisions_action_check;
alter table public.owner_decisions add constraint owner_decisions_action_check check (action = any (array[
  'accept','redo','to_montage','scene_not_needed','tv_drop_task','tv_mark_status','owner_task','in_film',
  'queue_up','queue_down','queue_remove','queue_add','ref_feedback']::text[]));
alter table public.owner_decisions drop constraint owner_decisions_shape_check;
alter table public.owner_decisions add constraint owner_decisions_shape_check check (
  ((action = 'owner_task') and note is not null and char_length(btrim(note)) >= 3)
  or ((action = 'ref_feedback') and note is not null and char_length(btrim(note)) >= 3)
  or ((action not in ('owner_task','ref_feedback')) and scene_id is not null));
