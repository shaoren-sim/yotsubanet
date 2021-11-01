import importlib
import os

def extract_labels_and_jobs_from_session(path_to_session_config: str):
    labels, scraper_jobs = parse_session_config(path_to_session_config)
    scraper_jobs = unpack_jobs(scraper_jobs)
    parsed_jobs = parse_jobs(scraper_jobs)

    return labels, parsed_jobs

def parse_session_config(path_to_session_config):
    module_load_string = os.path.splitext('.'.join(path_to_session_config.split(os.path.sep)))[0]
    module = importlib.import_module(module_load_string)

    return module.LABELS, module.SCRAPER_JOBS

def unpack_jobs(jobs_list):
    return_job = []
    for job in jobs_list:
        _type = job["TYPE"]
        for  (_subreddit, _search_query, _thread_flair, _label) in zip(job["SUBREDDIT"], job["SEARCH_QUERY"], job["THREAD_FLAIR"], job["LABEL"],):
            return_job.append(
                {
                    "TYPE": _type,
                    "SUBREDDIT": _subreddit,
                    "SEARCH_QUERY": _search_query,
                    "THREAD_FLAIR": _thread_flair,
                    "LABEL": _label
                }
            )
    return return_job

def parse_jobs(jobs_list):
    list_of_job_args = []
    for job in jobs_list:
        list_of_job_args.append(tuple([job[key] for key in job.keys()]))
    return list_of_job_args

if __name__ == "__main__":
    labels, jobs = extract_labels_and_jobs_from_session("webscraper_session/gotoubun_no_hanayome.py")
    print(labels)
    print(jobs)