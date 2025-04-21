import sqlite3
import datetime
import uuid
import pandas as pd
import os

# 결과 저장을 위한 폴더 생성
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# SQLite DB 초기화
def init_db():
    ensure_dir("Result")  # Result 폴더 생성
    conn = sqlite3.connect('similarity_results.db')
    c = conn.cursor()
    
    # 기존 테이블의 존재 여부 확인
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='results'")
    table_exists = c.fetchone()
    
    if not table_exists:
        # 테이블이 없으면 새로 생성
        c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            real_image_path TEXT,
            ai_image_path TEXT,
            ssim_score REAL,
            psnr_score REAL,
            vgg_score REAL,
            avg_score REAL,
            comment TEXT DEFAULT NULL
        )
        ''')
    else:
        # 테이블이 존재하면 comment 컬럼이 있는지 확인
        c.execute("PRAGMA table_info(results)")
        columns = c.fetchall()
        column_names = [column[1] for column in columns]
        
        # comment 컬럼이 없으면 추가
        if 'comment' not in column_names:
            c.execute("ALTER TABLE results ADD COLUMN comment TEXT DEFAULT NULL")
    
    conn.commit()
    conn.close()

# DB에 결과 저장
def save_results(real_image_path, ai_image_path, ssim_score, psnr_score, vgg_score, avg_score):
    conn = sqlite3.connect('similarity_results.db')
    c = conn.cursor()
    result_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()
    c.execute('''
    INSERT INTO results (id, timestamp, real_image_path, ai_image_path, ssim_score, psnr_score, vgg_score, avg_score)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (result_id, timestamp, real_image_path, ai_image_path, ssim_score, psnr_score, vgg_score, avg_score))
    conn.commit()
    conn.close()
    return result_id

# DB에서 결과 가져오기
def get_results():
    conn = sqlite3.connect('similarity_results.db')
    query = "SELECT * FROM results ORDER BY timestamp DESC"
    try:
        results = pd.read_sql(query, conn)
    except:
        results = pd.DataFrame(columns=["id", "timestamp", "real_image_path", "ai_image_path", "ssim_score", "psnr_score", "vgg_score", "avg_score", "comment"])
    conn.close()
    return results

# 결과에 코멘트 저장 함수 추가
def save_comment(result_id, comment):
    """
    결과에 코멘트를 저장하는 함수
    
    Args:
        result_id (str): 결과 ID
        comment (str): 저장할 코멘트
    
    Returns:
        bool: 저장 성공 여부
    """
    conn = sqlite3.connect('similarity_results.db')
    c = conn.cursor()
    c.execute("UPDATE results SET comment = ? WHERE id = ?", (comment, result_id))
    conn.commit()
    conn.close()
    return True