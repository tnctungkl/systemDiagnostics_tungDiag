select * from system_logs;

delete from system_logs;

CREATE OR REPLACE FUNCTION reset_system_logs_id_seq()
RETURNS TRIGGER AS $$
BEGIN
  IF (SELECT COUNT(*) FROM system_logs) = 0 THEN
    RETURN NULL;
  END IF;
  PERFORM setval('system_logs_id_seq', COALESCE((SELECT MAX(id) FROM system_logs), 0) + 1, false);
  RAISE NOTICE 'Sequence is reset!';
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_reset_system_logs_seq ON system_logs;

CREATE TRIGGER trg_reset_system_logs_seq
AFTER DELETE ON system_logs
FOR EACH STATEMENT
EXECUTE FUNCTION reset_system_logs_id_seq();