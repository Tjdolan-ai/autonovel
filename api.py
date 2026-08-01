#!/usr/bin/env python3
"""
Shared HTTP helper for the generator scripts.

A full pipeline run is 15-30 hours of API time, so a single transient 429 or
529 should not abort a phase. This wraps httpx.post with bounded retries on
the errors that are worth retrying, and leaves everything else to raise.
"""
import sys
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import httpx

# Statuses worth another attempt: rate limits, overloaded, transient upstream.
RETRY_STATUS = {408, 409, 429, 500, 502, 503, 504, 529}

MAX_ATTEMPTS = 4
BASE_BACKOFF = 2.0  # seconds; doubles each attempt (2, 4, 8)
MAX_RETRY_AFTER = 300.0  # cap, so an absurd header can't stall the pipeline


def retry_after_seconds(resp, default):
    """
    Honour a Retry-After header when the server sends one.

    RFC 9110 allows either delay-seconds or an HTTP-date; accept both, and
    fall back to the caller's backoff when the header is absent or unparseable.
    """
    raw = resp.headers.get("retry-after", "").strip()
    if not raw:
        return default

    try:
        return min(max(float(raw), 0.0), MAX_RETRY_AFTER)
    except (TypeError, ValueError):
        pass

    try:
        when = parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        return default
    if when is None:
        return default
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    delta = (when - datetime.now(timezone.utc)).total_seconds()
    return min(max(delta, 0.0), MAX_RETRY_AFTER)


def post_with_retry(url, *, headers, json, timeout,
                    max_attempts=MAX_ATTEMPTS, label="request"):
    """
    POST with exponential backoff on transient failures.

    Returns the successful httpx.Response. Raises the final exception if every
    attempt fails, so callers keep their existing error handling.
    """
    delay = BASE_BACKOFF
    last_exc = None

    for attempt in range(1, max_attempts + 1):
        try:
            resp = httpx.post(url, headers=headers, json=json, timeout=timeout)
            if resp.status_code in RETRY_STATUS and attempt < max_attempts:
                wait = retry_after_seconds(resp, delay)
                print(f"  {label}: HTTP {resp.status_code}, retrying in {wait:.0f}s "
                      f"(attempt {attempt}/{max_attempts})", file=sys.stderr)
                time.sleep(wait)
                delay *= 2
                continue
            resp.raise_for_status()
            return resp
        except (httpx.TransportError, httpx.TimeoutException) as e:
            last_exc = e
            if attempt >= max_attempts:
                break
            print(f"  {label}: {type(e).__name__}, retrying in {delay:.0f}s "
                  f"(attempt {attempt}/{max_attempts})", file=sys.stderr)
            time.sleep(delay)
            delay *= 2

    if last_exc is not None:
        raise last_exc
    # Exhausted retries on a retryable status — surface it as an HTTP error.
    resp.raise_for_status()
    return resp
