from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


@app.route('/api/info', methods=['GET'])
def get_full_player_info():
    uid = request.args.get('uid')
    region = request.args.get('region', 'ind')

    if not uid:
        return jsonify({'error': 'UID is required'}), 400

    target_url = f'https://free-fire-api-five.vercel.app/api/v1/info?uid={uid}&region={region}'

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        ),
        'Accept': 'application/json',
    }

    try:
        response = requests.get(target_url, headers=headers, timeout=12)

        if response.status_code == 200:
            data = response.json()
            full_data = {
                'basicInfo': data.get('basicInfo', {}),
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
  
