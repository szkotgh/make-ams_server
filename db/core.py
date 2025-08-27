import os
import sqlite3
import threading
import time
from contextlib import contextmanager
from queue import Queue, Empty


class DBResultDTO():
    def __init__(self, success: bool, detail: str, data: dict = None):
        self.success = success
        self.data = data
        self.detail = detail


def _get_db_path() -> str:
    env_path = os.environ.get('DATABASE_PATH')
    if env_path and env_path.strip():
        return env_path
    return './db/database.db'


# 연결 풀 설정
_connection_pool = Queue(maxsize=10)
_pool_lock = threading.Lock()


def get_connection(max_retries=3, retry_delay=0.1):
    """데이터베이스 연결을 가져옵니다. 연결 풀에서 재사용 가능한 연결을 우선 사용합니다."""
    for attempt in range(max_retries):
        try:
            # 연결 풀에서 기존 연결 가져오기 시도
            try:
                conn = _connection_pool.get_nowait()
                try:
                    # 연결이 여전히 유효한지 확인
                    conn.execute('SELECT 1')
                    return conn
                except (sqlite3.OperationalError, sqlite3.DatabaseError):
                    # 연결이 유효하지 않으면 닫고 새로 생성
                    try:
                        conn.close()
                    except:
                        pass
            except Empty:
                pass
            
            # 새 연결 생성
            conn = sqlite3.connect(_get_db_path(), timeout=30.0)  # 30초 타임아웃
            conn.row_factory = sqlite3.Row
            
            # 성능 및 동시성 개선을 위한 PRAGMA 설정
            try:
                conn.execute('PRAGMA foreign_keys = ON;')
                conn.execute('PRAGMA journal_mode = WAL;')  # WAL 모드로 동시 접근 성능 향상
                conn.execute('PRAGMA synchronous = NORMAL;')  # 성능과 안전성의 균형
                conn.execute('PRAGMA cache_size = 10000;')  # 캐시 크기 증가
                conn.execute('PRAGMA temp_store = MEMORY;')  # 임시 테이블을 메모리에 저장
                conn.execute('PRAGMA mmap_size = 268435456;')  # 메모리 매핑 크기 설정 (256MB)
                conn.execute('PRAGMA busy_timeout = 30000;')  # 30초 동안 잠금 대기
            except Exception:
                pass
            
            return conn
            
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e).lower() and attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  # 지수 백오프
                continue
            else:
                raise e
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))
                continue
            else:
                raise e
    
    raise Exception("Failed to get database connection after multiple retries")


def close_connection(conn):
    """데이터베이스 연결을 닫거나 연결 풀로 반환합니다."""
    if conn:
        try:
            # 연결이 유효한지 확인
            conn.execute('SELECT 1')
            
            # 연결 풀에 반환 시도
            try:
                _connection_pool.put_nowait(conn)
                return
            except:
                pass
        except:
            pass
        
        # 연결 풀이 가득 찼거나 연결이 유효하지 않으면 닫기
        try:
            conn.close()
        except:
            pass


@contextmanager
def connect(max_retries=3):
    """데이터베이스 연결을 위한 컨텍스트 매니저입니다."""
    conn = None
    for attempt in range(max_retries):
        try:
            conn = get_connection(max_retries=1)  # 연결 풀에서 가져올 때는 재시도하지 않음
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
                time.sleep(0.1 * (2 ** attempt))  # 지수 백오프
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
    """데이터베이스를 초기화합니다."""
    conn = get_connection()
    try:
        # Read SQL script from schema.sql file
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Execute SQL script
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
    """모든 데이터베이스 연결을 정리합니다."""
    with _pool_lock:
        while not _connection_pool.empty():
            try:
                conn = _connection_pool.get_nowait()
                try:
                    conn.close()
                except:
                    pass
            except Empty:
                break


def get_connection_info():
    """현재 연결 풀 상태를 반환합니다."""
    return {
        'pool_size': _connection_pool.qsize(),
        'max_size': _connection_pool.maxsize
    }


