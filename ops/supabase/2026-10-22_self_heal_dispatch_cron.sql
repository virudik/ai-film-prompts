-- 22.10.2026 (owner «да»): self-heal.yml via Supabase pg_cron, like the other robots. No secrets here.
-- Uses public.dispatch_github_workflow from 2026-10-13_robot_dispatch_cron.sql. Stop: select cron.unschedule('dispatch-self-heal');
select cron.schedule('dispatch-self-heal', '19,49 * * * *', $job$ select public.dispatch_github_workflow('self-heal.yml'); $job$);
