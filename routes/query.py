from flask import Blueprint, request, jsonify
import json
import utils.tasks as USER
from utils.auth_utils import token_required
from utils.redis import *

query_bp = Blueprint('solution', __name__)

@query_bp.route('/api/query_solution', methods=['GET'])
def query_solution():
    try:
        solution_id = request.args.get('id', default=1, type=str)
        
        # Redis
        cache_key = f"solution:{solution_id}"
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return jsonify(json.loads(cached_result)), 200
        
        result = USER.query_solution(solution_id)
        # 将查询结果缓存到 Redis，设置过期时间为一小时
        redis_client.setex(cache_key, 3600, json.dumps(result))
        return jsonify(result), 200
    except KeyError:
        return jsonify({"error": "Solution ID is missing"}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while querying the solution", "details": str(e)}), 500

@query_bp.route('/api/query_paper', methods=['GET'])
def query_paper():
    try:
        paper_id = request.args.get('id', default=1, type=str)
        
        # Redis
        cache_key = f"paper:{paper_id}"
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return jsonify(json.loads(cached_result)), 200
        
        result = USER.query_paper(paper_id)
         # 将查询结果缓存到 Redis，设置过期时间为一小时
        redis_client.setex(cache_key, 3600, json.dumps(result))
        return jsonify(result), 200
    except KeyError:
        return jsonify({"error": "Paper ID is missing"}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while querying the paper", "details": str(e)}), 500
    
@query_bp.route('/api/user/query_liked_solutions', methods=['POST'])
@token_required
def query_liked_solution(current_user):
    try:
        data = request.json
        solution_ids = data.get('solution_ids', [])
        if not solution_ids or not isinstance(solution_ids, list):
            return jsonify({"error": "Solution IDs are missing or invalid"}), 400
        
        result = []
        for solution_id in solution_ids:
            cache_key = f"liked:{current_user['_id']}:{solution_id}"
            cached_liked = redis_client.get(cache_key)
            
            if cached_liked is not None:
                is_liked = cached_liked == '1'
            else:
                # 若缓存中没有，则查询数据库
                is_liked = USER.query_liked_solution(current_user['_id'], solution_id)
                # 缓存查询结果到 Redis，过期时间设置为 1 小时
                redis_client.setex(cache_key, 3600, '1' if is_liked else '0')
                
            result.append({
                'solution_id': solution_id,
                'isLiked': is_liked
            })
        return jsonify(result), 200
    except KeyError:
        return jsonify({"error": "Solution ID or User ID is missing"}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while querying the liked solution", "details": str(e)}), 500