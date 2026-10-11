from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Garena Client Headers simulator
GARENA_HEADERS = {
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 11; SM-A515F Build/RP1A.200720.012)',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Type': 'application/x-www-form-urlencoded'
}

@app.route('/api/info', methods=['GET'])
def get_player_info():
    uid = request.args.get('uid')
    region = request.args.get('region', 'ind').lower()

    if not uid:
        return jsonify({'error': 'UID is required'}), 400

    # ফ্রি ফায়ারের গেম সার্ভার এন্ডপয়েন্ট (Region ভিত্তিক)
    if region == 'ind':
        url = f'https://ff-profile-api-india.vercel.app/api/info?uid={uid}'
    else:
        url = f'https://ff-profile-api-india.vercel.app/api/info?uid={uid}&region={region}'

    try:
        # সরাসরি রিকোয়েস্ট পাঠানো
        response = requests.get(url, headers=GARENA_HEADERS, timeout=12)
        
        if response.status_code == 200:
            data = response.json()
            return jsonify(data), 200
        else:
            return jsonify({'error': 'Player profile not found or Garena server issue'}), 404

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Server request timeout'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
