from __future__ import annotations

import os
import getpass
import io
from typing import Union, IO

try:
    import psycopg
    from psycopg.types.json import Jsonb as Json
except ImportError:
    import psycopg2 as psycopg
    from psycopg2.extras import Json as Json
from services.pdf_extraction_service import PdfExtractionService

def _build_conn_params():
    """Build database connection parameters.
    
    Priority: DATABASE_URL environment variable, then individual PG* variables.
    Supports passwordless connections for local trust/peer authentication.
    """
    dsn = os.getenv("DATABASE_URL")
    if dsn:
        return {"dsn": dsn}
    
    # Build connection parameters with fallback defaults
    params = dict(
        host=os.getenv("PGHOST", "localhost"),
        dbname=os.getenv("PGDATABASE", "easyxdb"),
        user=os.getenv("PGUSER", "easyxapp"),
        password=os.getenv("PGPASSWORD", "easyxpass"),  # Can be overridden by environment variable
        port=int(os.getenv("PGPORT", "5432")),
        connect_timeout=5,
    )
    
    # Filter out None or empty string values to avoid passing password parameter for passwordless connections
    return {k: v for k, v in params.items() if v not in (None, "")}

SQL_INSERT = """
INSERT INTO public.timesheet (meta_data, created_at, status)
VALUES (%s, NOW(), %s)
RETURNING tid, created_at;
"""

# Extensible: If table structure adds new columns (e.g., filename, pdf_text, notes), add corresponding SQL
SQL_INSERT_EXT = """
INSERT INTO public.timesheet (meta_data, created_at, status)
VALUES (%s, NOW(), %s)
RETURNING tid, created_at;
"""

PdfLike = Union[str, bytes, bytearray, IO[bytes]]

def _extract_meta_from_pdf(pdf_input: PdfLike) -> dict:
    """
    Extract structured metadata from PDF input.
    
    Accepts PDF file path, bytes, or binary file stream, returns structured metadata (dict).
    Prioritizes extractMeta method; falls back to extract_timesheet_data if structure validation fails.
    """
    svc = PdfExtractionService()

    def _run(stream: IO[bytes]) -> dict:
        # First try "complete metadata" extraction
        meta = svc.extractMeta(stream)
        
        # Handle extractMeta error responses
        if not isinstance(meta, dict) or meta.get("error"):
            # Rewind stream and fall back to lightweight extraction
            try:
                stream.seek(0)
            except Exception:
                pass
            
            meta_fallback = svc.extract_timesheet_data(stream)
            if isinstance(meta_fallback, dict) and not meta_fallback.get("error"):
                return meta_fallback
            
            # Both methods failed, raise error
            raise ValueError(
                f"PDF meta extraction failed: "
                f"{meta.get('error') if isinstance(meta, dict) else 'unknown error'} ; "
                f"fallback: {meta_fallback.get('error') if isinstance(meta_fallback, dict) else 'unknown error'}"
            )
        return meta

    # Input is a file path
    if isinstance(pdf_input, str):
        with open(pdf_input, "rb") as f:
            return _run(f)

    # Input is bytes/bytearray
    if isinstance(pdf_input, (bytes, bytearray)):
        with io.BytesIO(pdf_input) as bio:
            return _run(bio)

    # Input is a binary file stream (has read() method)
    if hasattr(pdf_input, "read"):
        # Try to ensure stream is re-readable
        if hasattr(pdf_input, "seek"):
            try:
                pdf_input.seek(0)
            except Exception:
                pass
        return _run(pdf_input) # type: ignore[arg-type]

    raise TypeError("pdf_input must be a file path, bytes/bytearray, or a binary file-like object")

def save_meta(meta_or_pdf: Union[dict, PdfLike], status: str = "done"):
    """
    Universal entry point for saving metadata to database.
    
    - Pass dict: save directly to database
    - Pass PDF path/bytes/file stream: automatically extract and save to database
    Returns: tid (primary key)
    """
    # 1) Parse metadata
    if isinstance(meta_or_pdf, dict):
        meta = meta_or_pdf
    else:
        meta = _extract_meta_from_pdf(meta_or_pdf)

    if not isinstance(meta, dict):
        raise TypeError("extracted meta must be a dict")

    # 2) Save to database
    conn_params = _build_conn_params()
    # When using context manager, psycopg3 will auto-commit on exit; explicitly enable autocommit for immediate visibility
    try:
        if "dsn" in conn_params:
            conn = psycopg.connect(conn_params["dsn"]) # type: ignore[index]
        else:
            conn = psycopg.connect(**conn_params) # type: ignore[arg-type]
        try:
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute(SQL_INSERT, (Json(meta), status))
                row = cur.fetchone()
                if not row:
                    raise RuntimeError("INSERT did not return tid")
                tid, created_at = row
                print(f"✅ saved: tid={tid}, created_at={created_at}, status={status}")
                return tid
        finally:
            try:
                conn.close()
            except Exception:
                pass
    except Exception as e:
        # Print connection and database info (without password) for troubleshooting
        safe = {k: v for k, v in conn_params.items() if k != 'password'}
        print(f"❌ save_meta failed. conn={safe}, error={e}")
        raise

def save_meta_with_extras(
    meta_or_pdf: Union[dict, PdfLike],
    *,
    status: str = "done",
    filename: str | None = None,
    pdf_text: str | None = None,
    notes: str | None = None,
):
    """
    Parse metadata and merge with additional information into JSONB (maintains single JSONB column for frontend/backend evolution).
    If future column separation is needed, can be changed to extend table structure and SQL.
    Returns: tid
    """
    if isinstance(meta_or_pdf, dict):
        meta = dict(meta_or_pdf)
    else:
        meta = _extract_meta_from_pdf(meta_or_pdf)

    if not isinstance(meta, dict):
        raise TypeError("extracted meta must be a dict")

    # Merge extras into meta envelope
    envelope = {
        "meta": meta,
        "extras": {
            "filename": filename,
            "pdf_text": pdf_text,
            "notes": notes,
        },
    }

    conn_params = _build_conn_params()
    try:
        if "dsn" in conn_params:
            conn = psycopg.connect(conn_params["dsn"]) # type: ignore[index]
        else:
            conn = psycopg.connect(**conn_params) # type: ignore[arg-type]
        try:
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute(SQL_INSERT_EXT, (Json(envelope), status))
                row = cur.fetchone()
                if not row:
                    raise RuntimeError("INSERT did not return tid")
                tid, created_at = row
                print(f"✅ saved with extras: tid={tid}, created_at={created_at}, status={status}")
                return tid
        finally:
            try:
                conn.close()
            except Exception:
                pass
    except Exception as e:
        safe = {k: v for k, v in conn_params.items() if k != 'password'}
        print(f"❌ save_meta_with_extras failed. conn={safe}, error={e}")
        raise

def extract_and_save(
    pdf_input: PdfLike,
    *,
    status: str = "done",
    keep_pdf_text: bool = False,
    filename: str | None = None,
    notes: str | None = None,
):
    """
    One-step process:
    - Input PDF (path/bytes/stream)
    - Extract metadata (prioritize extractMeta, fallback on failure)
    - Optionally extract full text pdf_text
    - Save to JSONB database, return tid
    """
    svc = PdfExtractionService()

    # Get re-readable stream
    def _as_stream(inp: PdfLike) -> IO[bytes]:
        if isinstance(inp, str):
            return open(inp, "rb")
        if isinstance(inp, (bytes, bytearray)):
            return io.BytesIO(inp)
        if hasattr(inp, "read"):
            return inp # type: ignore[return-value]
        raise TypeError("pdf_input must be a path/bytes/file-like")

    stream = _as_stream(pdf_input)
    try:
        # First extract metadata
        # Use internal logic to ensure fallback strategy
        meta = _extract_meta_from_pdf(stream)

        # Optionally extract full text
        text_value = None
        if keep_pdf_text:
            try:
                if hasattr(stream, "seek"):
                    stream.seek(0)
                text_value = svc.get_pdf_text(stream)
            except Exception:
                text_value = None

        return save_meta_with_extras(
            meta,
            status=status,
            filename=filename,
            pdf_text=text_value,
            notes=notes,
        )
    finally:
        try:
            # Only close file handles that we opened
            if isinstance(pdf_input, str):
                stream.close()
        except Exception:
            pass
