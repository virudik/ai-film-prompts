-- Reliable external trigger for the GitHub robot (owner-approved 13.10.2026).
-- WHY: GitHub's own `schedule:` cron proved unreliable here (gaps of 5-7 hours instead of 30 minutes).
-- Supabase pg_cron fires on time and calls GitHub's workflow_dispatch API.
-- The GitHub token (fine-grained, ONE repo, permission "Actions: Read and write" only) lives in Supabase Vault
-- under the name `github_dispatch_token`; it is NEVER written into SQL, git, chat or logs.
-- Applied via Supabase migrations: robot_dispatch_cron_topview_robot, robot_dispatch_cron_sync_and_archive.

create extension if not exists pg_net with schema extensions;
create extension if not exists pg_cron with schema pg_catalog;

create or replace function public.dispatch_github_workflow(workflow_file text)
returns bigint
language plpgsql
security definer
set search_path = ''
as $fn$
declare
  tok text;
  req_id bigint;
begin
  select decrypted_secret into tok from vault.decrypted_secrets where name = 'github_dispatch_token';
  if tok is null then
    raise exception 'github_dispatch_token missing in vault';
  end if;
  select net.http_post(
    url := 'https://api.github.com/repos/virudik/ai-film-prompts/actions/workflows/' || workflow_file || '/dispatches',
    headers := jsonb_build_object(
      'Authorization', 'Bearer ' || tok,
      'Accept', 'application/vnd.github+json',
      'X-GitHub-Api-Version', '2022-11-28',
      'User-Agent', 'supabase-cron-robot',
      'Content-Type', 'application/json'),
    body := '{"ref":"main"}'::jsonb
  ) into req_id;
  return req_id;
end
$fn$;

revoke all on function public.dispatch_github_workflow(text) from public, anon, authenticated;

-- offsets keep the three runs from starting together
select cron.schedule('dispatch-topview-robot',         '*/10 * * * *',    $job$ select public.dispatch_github_workflow('topview-robot.yml'); $job$);
select cron.schedule('dispatch-sync-from-drive',       '2-59/10 * * * *', $job$ select public.dispatch_github_workflow('sync-from-drive.yml'); $job$);
select cron.schedule('dispatch-topview-video-archive', '5-59/10 * * * *', $job$ select public.dispatch_github_workflow('topview-video-archive.yml'); $job$);

-- Stop one:  select cron.unschedule('dispatch-topview-robot');
-- If a workflow file is renamed, re-create its job with the new file name.
-- Check:     select jobname, schedule, active from cron.job;
--            select status_code, count(*) from net._http_response group by 1;  -- 204 = accepted by GitHub
