import praw
import re

# Regex checks
# Django URL regex source
url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

reddit_link_regex = re.compile('(?<=\[).*?\].*?.*?\(.*?.(?=\))')
square_bracket_regex = re.compile('(?<=\[)(.*?)(?=\])')
bracket_regex = re.compile('(?<=\()(.*?)(?=\))')

# https://stackoverflow.com/questions/1007481/how-do-i-replace-whitespaces-with-underscore
def strip_and_lowercase(s):
    s = s.lower()
    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)
    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '_', s)

    return s

def extract_links_from_comments(comment):
    # Extract links from comment.
    links_in_comments =  [f"[{links_in_comment})" for links_in_comment in reddit_link_regex.findall(comment)]
    if len(links_in_comments) == 0:
        return [], [], []
    links_in_comments = sanitize_comments(links_in_comments)

    link_texts = [square_bracket_regex.findall(link)[0] for link in links_in_comments]
    urls = [bracket_regex.findall(link)[0] for link in links_in_comments]

    return links_in_comments, link_texts, urls

def sanitize_comments(list_of_links):
    """Sanitizier that removes comment faces, necessary for r/anime comments."""
    for link in list_of_links:
        print(link)
        if len(square_bracket_regex.findall(link)) == 0:
            list_of_links.remove(link)
            continue
        elif len(square_bracket_regex.findall(link)[0]) == 0:
            list_of_links.remove(link)
            continue
        elif re.match(url_regex, bracket_regex.findall(link)[0]) is None:
            list_of_links.remove(link)
            continue
    return list_of_links

class RedditPrawler():
    def __init__(
        self,
        client_id,          # your client id
        client_secret,      #your client secret
        user_agent,  #user agent name
        username,           # your reddit username
        password,
        check_for_async=False     # your reddit password
    ):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password,
            check_for_async=check_for_async,
        )
    
    def subreddit(self, subreddit_name):
        subreddit = self.reddit.subreddit(subreddit_name)
        return subreddit

    def search_for_threads(
        self, 
        subreddit_name, 
        search_string
        ):
        if type(subreddit_name) is praw.models.reddit.subreddit.Subreddit:
            subreddit = subreddit_name
        elif type(subreddit_name) is str:
            subreddit = self.reddit.subreddit(subreddit_name)
        else:
            raise ValueError("subreddit name must be string or a praw.models.reddit.subreddit.Subreddit object.")
        results = list(subreddit.search(search_string))
        print(f"{len(results)} threads found.")

        return results

    def get_comments(self, reddit_thread):
        return reddit_thread.comments