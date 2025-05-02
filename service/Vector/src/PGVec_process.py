import psycopg2
import json
import numpy as np

class PGVecProcess:
    
    def __init__(self, params=None):
        """
        PGVector 처리를 위한 클래스 초기화
        
        :param params: 데이터베이스 연결 파라미터
        """
        self.params = params or {
            "dbname": "mydatabase",
            "user": "myuser",
            "password": "mypassword",
            "host": "localhost",
            "port" : "5433"
        }
        
        # 데이터베이스 연결 메서드 추가
        self.conn = None
    
    def connect(self):
        """데이터베이스 연결을 설정"""
        try:
            self.conn = psycopg2.connect(**self.params)
            return self.conn.cursor()
        except Exception as e:
            print(f"데이터베이스 연결 중 오류 발생: {e}")
            return None
    
    def close(self):
        """데이터베이스 연결을 닫습니다."""
        if self.conn:
            self.conn.close()
    
    def injection(self, data, cursor):
        """
        데이터 삽입
        
        :param data: 삽입할 데이터 딕셔너리
        :param cursor: 데이터베이스 커서
        :return: 삽입 성공 여부
        """
        try:
            # 데이터 추출
            source_url = data['input'].get('image', '')
            embedding = data.get('embedding', None)  # 임베딩 벡터
            
            # embedding이 numpy 배열인 경우 적절한 형태로 변환
            if isinstance(embedding, np.ndarray):
                embedding = embedding.tolist()
                
            # 메타데이터 추출
            metadata = {
                'season': data['input'].get('season', ''),
                'category': data['input'].get('category', ''),
                'sub_category': data['input'].get('sub_category', ''),
                'color': data['input'].get('color', '')
            }

            # 추천 정보 추출
            output = data.get('output', {})
            answer = output.get('answer', '')
            recommend = json.dumps(output.get('recommend', {}))
        
            # 삽입 쿼리 - pgvector 형식으로 변환
            insert_query = """
            INSERT INTO fashion_recommendations 
            (source_url, embedding, season, category, sub_category, color, answer, recommend)
            VALUES (%s, %s::vector, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (source_url) DO UPDATE SET
            embedding = EXCLUDED.embedding,
            season = EXCLUDED.season,
            category = EXCLUDED.category,
            sub_category = EXCLUDED.sub_category,
            color = EXCLUDED.color,
            answer = EXCLUDED.answer,
            recommend = EXCLUDED.recommend
            """
            
            # 쿼리 실행
            cursor.execute(insert_query, (
                source_url, 
                embedding, 
                metadata['season'], 
                metadata['category'], 
                metadata['sub_category'], 
                metadata['color'], 
                answer, 
                recommend
            ))
            
            # 트랜잭션 커밋
            self.conn.commit()
            return True
        
        except Exception as e:
            # 오류 발생 시 롤백
            if self.conn:
                self.conn.rollback()
            print(f"데이터 삽입 중 오류 발생: {e}")
            return False
            
    def similarity_search(self, embedding, cursor, top_k=5):
        """
        주어진 임베딩과 가장 유사한 벡터 검색
        
        :param embedding: 검색할 임베딩 벡터
        :param cursor: 데이터베이스 커서
        :param top_k: 반환할 최상위 유사 항목 수
        :return: 유사한 항목 리스트
        """
        try:
            # numpy 배열을 리스트로 변환
            if isinstance(embedding, np.ndarray):
                embedding = embedding.tolist()
                
            # 유사도 검색 쿼리
            query = """
            SELECT 
                source_url, 
                embedding, 
                season,
                category,
                sub_category,
                color,
                answer,
                recommend,
                embedding <-> %s::vector AS distance
            FROM fashion_recommendations
            ORDER BY distance
            LIMIT %s
            """
            
            # 쿼리 실행
            cursor.execute(query, (embedding, top_k))
            
            # 결과 변환
            results = []
            for row in cursor.fetchall():
                # recommend 필드 안전하게 처리
                recommend_data = {}
                if row[7]:
                    if isinstance(row[7], str):
                        try:
                            recommend_data = json.loads(row[7])
                        except json.JSONDecodeError:
                            recommend_data = {"error": "잘못된 JSON 형식"}
                    elif isinstance(row[7], dict):
                        recommend_data = row[7]  
                
                distance = float(row[8])
                max_distance = 10.0
                similarity_percentage = max(0, 100 * (1 - distance / max_distance))

                results.append({
                    'source_url': row[0],
                    'embedding': row[1],
                    'season': row[2],
                    'category': row[3],
                    'sub_category': row[4],
                    'color': row[5],
                    'answer': row[6],
                    'recommend': recommend_data,
                    'distance': row[8],
                    'similarity': round(similarity_percentage, 2)
                })
            
            return results
        
        except Exception as e:
            print(f"유사도 검색 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()  # 자세한 오류 추적
            return []