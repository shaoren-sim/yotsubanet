from webscraper.reddit_scraper import RedditPrawler, reddit_link_regex, square_bracket_regex, bracket_regex, extract_links_from_comments
from config.reddit_praw_login_details import RedditLoginDetails

if __name__ == "__main__":
    print("Test 1: Try linking to the custom prawler object.")
    client_id = RedditLoginDetails.client_id
    client_secret = RedditLoginDetails.client_secret
    user_agent = RedditLoginDetails.user_agent
    username = RedditLoginDetails.username
    password = RedditLoginDetails.password
    reddit = RedditPrawler(
        client_id=client_id,      # your client id
        client_secret=client_secret,  #your client secret
        user_agent=user_agent, #user agent name
        username=username,     # your reddit username
        password=password,
        check_for_async=False     # your reddit password
        )

    sub = 'anime'
    subreddit = reddit.subreddit(sub)
    print(subreddit.display_name)
    print(subreddit.title)
    # print(subreddit.description)

    print("Test 2: Testing thread search.")
    goutoubun_s2_discussion_threads = reddit.search_for_threads(subreddit, "Go-toubun no Hanayome ∬ Episode Discussion")
    for thread in goutoubun_s2_discussion_threads:
        print(type(thread))
        print(thread.title)
    
    goutoubun_s1_discussion_threads = reddit.search_for_threads(subreddit, "Go-toubun no Hanayome Episode Discussion")
    for thread in goutoubun_s1_discussion_threads:
        print(thread.title)

    print("Test 3: Testing comment extraction.")
    discussion_thread = goutoubun_s2_discussion_threads[4]

    thread_comments = reddit.get_comments(discussion_thread)[10]
    print(thread_comments)

    # Testing regex links
    print("Test 4: Testing regex.")
    comment = "Hello this is my [website](https://www.google.com)"
    reddit_link = [f"[{links_in_comment})" for links_in_comment in reddit_link_regex.findall(comment)]
    print(reddit_link)

    link_text = [square_bracket_regex.findall(link)[0] for link in reddit_link]
    print(link_text)

    url = [bracket_regex.findall(link)[0] for link in reddit_link]
    print(url)

    # Skipping first comment becasuse it is the spoiler reminer
    for comment_body in discussion_thread.comments[1:]:
        comment_text = comment_body.body
        if extract_links_from_comments(comment_text) is not None:
            comment = comment_text
            break
    print(comment)

    # Extract links from comment.
    links_in_comment, link_texts, urls = extract_links_from_comments(comment)

    print("Test 5: Testing link extraction function.")
    for reddit_link, link_text, url in zip(links_in_comment, link_texts, urls):
        print(reddit_link)
        print(link_text)
        print(url)
        print('-'*12)