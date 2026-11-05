import requests
import random

def get_public_domain_movies(limit=20):
    # كنقلبو على أفلام فـ الملكية العامة اللي عندهم ملفات MP4
    url = f"https://archive.org/advancedsearch.php?q=collection%3Afeature_films+AND+mediatype%3Amovies&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=description&fl%5B%5D=year&rows={limit}&page=1&output=json"
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        docs = response.json().get('response', {}).get('docs', [])
        
        movies = []
        for doc in docs:
            identifier = doc.get('identifier')
            if not identifier: continue
            
            # نجيبو معلومات الفيلم بالتفصيل باش نلقاو رابط الـ MP4
            meta_url = f"https://archive.org/metadata/{identifier}"
            meta_res = requests.get(meta_url, timeout=15).json()
            
            if 'files' not in meta_res: continue
            
            # كنقلبو على ملف الفيديو
            video_file = None
            for f in meta_res['files']:
                if f['name'].endswith('.mp4') or f['name'].endswith('.mpeg4'):
                    video_file = f['name']
                    break
                    
            if video_file:
                movies.append({
                    'title': doc.get('title', 'Unknown Title'),
                    'description': doc.get('description', 'No description available.'),
                    'year': doc.get('year', 'N/A'),
                    'video_url': f"https://archive.org/download/{identifier}/{video_file}"
                })
        return movies
    except Exception as e:
        print(f"Error fetching from Archive.org: {e}")
        return []
