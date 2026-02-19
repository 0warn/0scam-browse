import re
import math
from urllib.parse import urlparse
import numpy as np

class URLFeatureExtractor:
    def __init__(self):
        self.suspicious_keywords = [
            'login', 'verify', 'secure', 'update', 'account', 'banking', 
            'confirm', 'signin', 'wallet', 'crypto', 'paypal', 'apple', 
            'microsoft', 'google', 'outlook', 'amazon', 'ebay', 'walmart',
            'stock', 'market', 'price', 'bonus', 'free', 'gift', 'win',
            'verification', 'webscr', 'cmd', 'dispatch', 'submit'
        ]
        self.common_tlds = ['.com', '.org', '.net', '.edu', '.gov', '.io', '.co', '.uk', '.ca', '.de', '.jp', '.fr', '.au']

    def get_entropy(self, text):
        if not text: return 0
        prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
        return entropy

    def extract_features(self, url):
        features = []
        try:
            parsed_url = urlparse(url)
            hostname = parsed_url.netloc
            path = parsed_url.path
            lower_url = url.lower()
            
            # 1. URL Length
            features.append(len(url))
            
            # 2. Hostname Length
            features.append(len(hostname))
            
            # 3. Number of dots in URL
            features.append(url.count('.'))
            
            # 4. Subdomain depth
            features.append(max(0, hostname.count('.') - 1)) 
            
            # 5. Presence of IP address
            ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
            features.append(1 if ip_pattern.match(hostname) else 0)
            
            # 6. HTTPS usage
            features.append(1 if parsed_url.scheme == 'https' else 0)
            
            # 7. @ count
            features.append(url.count('@'))
            # 8. - count
            features.append(url.count('-'))
            # 9. _ count
            features.append(url.count('_'))
            # 10. // count
            features.append(url.count('//'))
            # 11. ? count
            features.append(url.count('?'))
            # 12. = count
            features.append(url.count('='))
            # 13. % count
            features.append(url.count('%'))
            
            # 14. Digit count
            digit_count = sum(c.isdigit() for c in url)
            features.append(digit_count)
            
            # 15. Hostname entropy
            features.append(self.get_entropy(hostname))
            
            # 16. Keywords count
            keyword_count = 0
            for keyword in self.suspicious_keywords:
                if keyword in lower_url:
                    keyword_count += 1
            features.append(keyword_count)
            
            # 17. Uncommon TLD
            has_common_tld = any(hostname.lower().endswith(tld) for tld in self.common_tlds)
            features.append(0 if has_common_tld else 1)

            # 18. Short URL
            shorteners = ['bit.ly', 'goo.gl', 'shorte.st', 'go2l.ink', 'x.co', 'ow.ly', 't.co', 'tinyurl.com']
            features.append(1 if any(s in hostname.lower() for s in shorteners) else 0)

            # 19. Vowel ratio
            vowels = "aeiou"
            v_count = sum(hostname.count(v) for v in vowels)
            c_count = len(re.sub(r'[^a-z]', '', hostname.lower())) - v_count
            features.append(v_count / (c_count + 1))

        except Exception as e:
            return [0] * 19

        return features

    def get_feature_names(self):
        return [
            "url_len", "host_len", "dots", "subdomains", "is_ip", "is_https",
            "at", "hyphen", "underscore", "dbl_slash", "ques", "equal", "percent",
            "digits", "entropy", "keywords", "uncommon_tld", "shortened", "vowel_ratio"
        ]
