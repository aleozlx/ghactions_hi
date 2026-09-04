#!/usr/bin/env bash
# Verbatim replica of the upstream/main "Parse command" step.
COMMENT_BODY="$(cat)"
if echo "$COMMENT_BODY" | grep -qi "@flashinfer-bot rerun failed"; then
  echo "rerun-failed"
elif echo "$COMMENT_BODY" | grep -qi "@flashinfer-bot rerun"; then
  echo "rerun"
elif echo "$COMMENT_BODY" | grep -qi "@flashinfer-bot stop"; then
  echo "stop"
elif echo "$COMMENT_BODY" | grep -qi "@flashinfer-bot run"; then
  echo "run"
else
  echo "unknown"
fi
