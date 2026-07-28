# Use recoverable Resume upload operations

Resume uploads use idempotency records bound to authenticated user, operation and target, SHA-256 file content, detected document type, and file size. Completed and deterministic rejected records are retained for 24 hours; a processing lease inactive for 30 minutes becomes `retryable_failure`, and an explicit retry with the same key and file may acquire a new fenced lease so the stale worker cannot commit.

A duplicate request during processing returns `202 upload_in_progress` with an owned status URL and retry guidance rather than starting extraction. Status checks may continue automatically because they do not retransmit the file; upload retry remains explicit. More than one multipart file returns `400 multiple_files_not_allowed` before extraction or profile mutation.
