-- ---------- 1) create timesheet if not exists ----------
CREATE TABLE IF NOT EXISTS timesheet (
  tid        SERIAL PRIMARY KEY,
  meta_data  JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  status     TEXT
);

-- ---------- 2) insert 10 default data if table is empty ----------
INSERT INTO timesheet (meta_data, created_at, status)
SELECT
  jsonb_build_object('note', format('seed row %s', gs))            AS meta_data,
  now() - (gs || ' hours')::interval                               AS created_at,
  (ARRAY['in-progress','done','pending'])[1 + (gs % 3)]            AS status
FROM generate_series(1, 10) AS gs
WHERE NOT EXISTS (SELECT 1 FROM timesheet);