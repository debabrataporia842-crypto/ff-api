from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/api/info', methods=['GET'])
def get_full_player_info():
    uid = request.args.get('uid')
    region = request.args.get('region', 'ind')

    if not uid:
        return jsonify({'error': 'UID is required'}), 400

    # বিকল্প এবং সচল একটি ফ্রি ফায়ার API এন্ডপয়েন্ট
    target_url = f'https://ff-api-endpoint.vercel.app/api/info?uid={uid}&region={region}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
    }

    try:
        response = requests.get(target_url, headers=headers, timeout=12)

        if response.status_code == 200:
            data = response.json()
            # যদি ডেটা সরাসরি রুট অবজেক্টে বা basicInfo তে থাকে
            basic = data.get('basicInfo', data)
            
            full_data = {
                'basicInfo': basic,
                'clanBasicInfo': data.get('clanBasicInfo', {}),
                'socialInfo': data.get('socialInfo', {}),
                'captainBasicInfo': data.get('captainBasicInfo', {}),
                'creditScoreInfo': data.get('creditScoreInfo', {}),
                'petInfo': data.get('petInfo', {}),
            }
            return jsonify(full_data), 200
        else:
            return jsonify({'error': 'Player profile not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
  
