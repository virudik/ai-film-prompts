-- AI Film: free-text owner tasks from the site (action owner_task) + triage statuses.
-- Applied to Supabase project vzohfatqzyioydtgjiyd only with the owner's explicit OK.
alter table public.owner_decisions alter column scene_id drop not null;
alter table public.owner_decisions drop constraint owner_decisions_scene_id_check;
alter table public.owner_decisions add constraint owner_decisions_scene_id_check check (scene_id is null or (scene_id >= 1 and scene_id <= 999));
alter table public.owner_decisions drop constraint owner_decisions_action_check;
alter table public.owner_decisions add constraint owner_decisions_action_check check (action = any (array['accept','redo','to_montage','scene_not_needed','tv_drop_task','tv_mark_status','owner_task']));
alter table public.owner_decisions drop constraint owner_decisions_note_check;
alter table public.owner_decisions add constraint owner_decisions_note_check check (note is null or char_length(note) <= 2000);
alter table public.owner_decisions drop constraint owner_decisions_status_check;
alter table public.owner_decisions add constraint owner_decisions_status_check check (status = any (array['pending','in_progress','needs_owner','applied','rejected','superseded']));
alter table public.owner_decisions add constraint owner_decisions_shape_check check (
  (action = 'owner_task' and note is not null and char_length(btrim(note)) >= 3)
  or (action <> 'owner_task' and scene_id is not null));
