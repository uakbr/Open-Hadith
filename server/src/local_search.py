import json
import os
from typing import List, Dict, Any
import functools


class LocalHadithSearch:
    """
    Local JSON-based hadith search implementation
    """
    
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), '../../data')
        self.search_index = self._load_search_index()
        self.collections = self._load_collections()
    
    def _load_search_index(self) -> Dict:
        """Load the search index from JSON file"""
        index_path = os.path.join(self.data_path, 'search-index.json')
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _load_collections(self) -> Dict:
        """Load collections metadata"""
        collections_path = os.path.join(self.data_path, 'collections.json')
        if os.path.exists(collections_path):
            with open(collections_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {c['id']: c for c in data['collections']}
        return {}
    
    @functools.lru_cache(maxsize=512)
    def search_hadith(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search hadiths based on query string
        Returns list of matching hadiths with scores
        """
        if not query:
            return []
        
        query_lower = query.lower()
        results = []
        
        # Search through all collections in the index
        for collection_id, collection_data in self.search_index.get('collections', {}).items():
            collection_name = self.collections.get(collection_id, {}).get('name', collection_id)
            
            for book_id, book_data in collection_data.get('books', {}).items():
                book_name = book_data.get('bookName', '')
                
                for hadith in book_data.get('hadiths', []):
                    searchable_text = hadith.get('searchableText', '').lower()
                    
                    # Simple scoring based on occurrence count
                    score = searchable_text.count(query_lower)
                    
                    if score > 0:
                        # Format result similar to MongoDB response
                        result = {
                            'collection_id': collection_id,
                            'collection': collection_name,
                            'hadith_no': hadith.get('hadithNumber'),
                            'book_no': int(book_id),
                            'book_en': book_name,
                            'narrator_en': hadith.get('englishNarrated', ''),
                            'body_en': hadith.get('englishText', ''),
                            'body_ar': hadith.get('arabicText', ''),
                            'book_ref_no': hadith.get('bookReference'),
                            'score': score
                        }
                        results.append(result)
        
        # Sort by score (descending) and limit results
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:limit]
    
    def search_hadith_advanced(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Advanced search with highlighting and better scoring
        """
        if not query:
            return []
        
        query_words = query.lower().split()
        results = []
        
        for collection_id, collection_data in self.search_index.get('collections', {}).items():
            collection_name = self.collections.get(collection_id, {}).get('name', collection_id)
            
            for book_id, book_data in collection_data.get('books', {}).items():
                book_name = book_data.get('bookName', '')
                
                for hadith in book_data.get('hadiths', []):
                    searchable_text = hadith.get('searchableText', '').lower()
                    english_text = hadith.get('englishText', '')
                    
                    # Calculate score based on word matches
                    score = 0
                    highlights = []
                    
                    for word in query_words:
                        word_count = searchable_text.count(word)
                        if word_count > 0:
                            score += word_count
                            # Find positions for highlighting
                            start = 0
                            while True:
                                pos = searchable_text.find(word, start)
                                if pos == -1:
                                    break
                                highlights.append({
                                    'start': pos,
                                    'end': pos + len(word),
                                    'text': english_text[pos:pos+len(word)] if pos < len(english_text) else ''
                                })
                                start = pos + 1
                    
                    if score > 0:
                        result = {
                            'collection_id': collection_id,
                            'collection': collection_name,
                            'hadith_no': hadith.get('hadithNumber'),
                            'book_no': int(book_id),
                            'book_en': book_name,
                            'chapter_no': 1,  # Default value as it's not in the index
                            'chapter_en': '',  # Default value
                            'narrator_en': hadith.get('englishNarrated', ''),
                            'body_en': english_text,
                            'book_ref_no': str(hadith.get('bookReference', '')),
                            'hadith_grade': '',  # Default value
                            'score': score,
                            'highlights': highlights[:5]  # Limit highlights
                        }
                        results.append(result)
        
        # Sort by score (descending) and limit results
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:limit]
    
    def get_hadith_by_reference(self, collection_id: str, book_no: str, ref_no: str) -> Dict[str, Any]:
        """
        Get a specific hadith by its reference numbers
        """
        collection_data = self.search_index.get('collections', {}).get(collection_id, {})
        book_data = collection_data.get('books', {}).get(str(book_no), {})
        
        for hadith in book_data.get('hadiths', []):
            if str(hadith.get('bookReference')) == str(ref_no):
                collection_name = self.collections.get(collection_id, {}).get('name', collection_id)
                return {
                    'collection_id': collection_id,
                    'collection': collection_name,
                    'hadith_no': hadith.get('hadithNumber'),
                    'book_no': int(book_no),
                    'book_en': book_data.get('bookName', ''),
                    'narrator_en': hadith.get('englishNarrated', ''),
                    'body_en': hadith.get('englishText', ''),
                    'body_ar': hadith.get('arabicText', ''),
                    'book_ref_no': hadith.get('bookReference')
                }
        
        return None