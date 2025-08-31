import os
import sqlite3
import threading
import time
from contextlib import contextmanager
from queue import Queue, Empty
from dotenv import load_dotenv

load_dotenv()

class DBResultDTO():
    def __init__(self, success: bool, detail: str, data: dict = None):
        self.success = success
        self.data = data
        self.detail = detail


def _get_db_path() -> str:
    return "db/database.db"


_thread_local = threading.local()
_pool_lock = threading.Lock()


def _get_thread_pool():
    if not hasattr(_thread_local, 'connection_pool'):
        _thread_local.connection_pool = Queue(maxsize=10)
        _thread_local.connection_timestamps = {}
    return _thread_local.connection_pool, _thread_local.connection_timestamps


def get_connection(max_retries=3, retry_delay=0.05):
    for attempt in range(max_retries):
        try:
            pool, timestamps = _get_thread_pool()
            
            try:
                conn = pool.get_nowait()
                with _pool_lock:
                    if id(conn) in timestamps:
                        if time.time() - timestamps[id(conn)] < 300:
                            return conn
                        else:
                            del timestamps[id(conn)]
                            try:
                                conn.close()
                            except:
                                pass
                    else:
                        return conn
            except Empty:
                pass
            
            # 타임아웃을 5초로 더 줄여서 빠른 응답
            conn = sqlite3.connect(_get_db_path(), timeout=5.0)
            conn.row_factory = sqlite3.Row
            
            try:
                conn.execute('PRAGMA foreign_keys = ON;')
                conn.execute('PRAGMA journal_mode = WAL;')
                conn.execute('PRAGMA synchronous = NORMAL;')
                conn.execute('PRAGMA cache_size = 10000;')
                conn.execute('PRAGMA temp_store = MEMORY;')
                conn.execute('PRAGMA mmap_size = 268435456;')
                conn.execute('PRAGMA busy_timeout = 5000;')  # 5초로 줄임
            except Exception:
                pass
            
            with _pool_lock:
                timestamps[id(conn)] = time.time()
            
            return conn
            
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e).lower() and attempt < max_retries - 1:
                time.sleep(retry_delay)  # 고정된 짧은 대기 시간
                continue
            else:
                raise e
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)  # 고정된 짧은 대기 시간
                continue
            else:
                raise e
    
    raise Exception("Failed to get database connection after multiple retries")


def close_connection(conn):
    if conn:
        try:
            pool, timestamps = _get_thread_pool()
            
            try:
                pool.put_nowait(conn)
                return
            except:
                try:
                    old_conn = pool.get_nowait()
                    with _pool_lock:
                        if id(old_conn) in timestamps:
                            del timestamps[id(old_conn)]
                    old_conn.close()
                    pool.put_nowait(conn)
                    return
                except:
                    pass
        except:
            pass
        
        try:
            with _pool_lock:
                pool, timestamps = _get_thread_pool()
                if id(conn) in timestamps:
                    del timestamps[id(conn)]
            conn.close()
        except:
            pass


@contextmanager
def connect(max_retries=3):
    conn = None
    for attempt in range(max_retries):
        try:
            conn = get_connection(max_retries=1)
            yield conn
            conn.commit()
            break
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e).lower() and attempt < max_retries - 1:
                if conn:
                    try:
                        conn.rollback()
                    except:
                        pass
                time.sleep(0.1)
                continue
            else:
                if conn:
                    try:
                        conn.rollback()
                    except:
                        pass
                raise e
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            raise e
        finally:
            close_connection(conn)


def init_db():
    conn = get_connection()
    try:
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        conn.executescript(schema_sql)
        conn.commit()
    except Exception as e:
        print(f"Error occurred during database initialization: {e}")
        try:
            conn.rollback()
        except:
            pass
        raise
    finally:
        close_connection(conn)


def cleanup_connections():
    try:
        pool, timestamps = _get_thread_pool()
        with _pool_lock:
            while not pool.empty():
                try:
                    conn = pool.get_nowait()
                    try:
                        if id(conn) in timestamps:
                            del timestamps[id(conn)]
                        conn.close()
                    except:
                        pass
                except Empty:
                    break
            timestamps.clear()
    except:
        pass


def get_connection_info():
    try:
        pool, timestamps = _get_thread_pool()
        return {
            'pool_size': pool.qsize(),
            'max_size': pool.maxsize,
            'active_connections': len(timestamps),
            'thread_id': threading.get_ident()
        }
    except:
        return {
            'pool_size': 0,
            'max_size': 0,
            'active_connections': 0,
            'thread_id': threading.get_ident()
        }


