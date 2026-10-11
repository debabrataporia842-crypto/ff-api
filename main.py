from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/api/info', methods=['GET'])
def get_full_player_info():
    uid = request.args.get('uid')
    region = request.args.get('region', 'ind')

    if not uid:
        return jsonify({'error': 'UID is required'}), 400

    # ফ্রি ফায়ার প্লেয়ার ইনফো ফেচ করার সরাসরি সচল API
    target_url = f'https://free-fire-api-five.vercel.app/api/v1/info?uid={uid}&region={region}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
    }

    try:
        response = requests.get(target_url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            return jsonify(data), 200
        else:
            # অন্য একটি সচল ব্যাকআপ এন্ডপয়েন্ট দিয়ে চেষ্টা করা
            backup_url = f'https://ff-api-endpoint.vercel.app/api/info?uid={uid}&region={region}'
            res_backup = requests.get(backup_url, headers=headers, timeout=10)
            if res_backup.status_code == 200:
                return jsonify(res_backup.json()), 200
            
            return jsonify({'error': 'Player profile not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
