# %%
import importlib
import os
import json

def extract_labels_and_jobs_from_session(path_to_session_config: str):
    labels, scraper_jobs = parse_session_config(path_to_session_config)
    scraper_jobs = unpack_jobs(scraper_jobs)
    parsed_jobs = parse_jobs(scraper_jobs)

    return labels, parsed_jobs

def parse_session_config(path_to_session_config: str):
    session = read_session(path_to_session_config)

    return session["labels"], session["jobs"]

def unpack_jobs(jobs_list):
    return_job = []
    for job in jobs_list:
        _type = job["TYPE"]
        if type(job["SUBREDDIT"]) == list and type(job["SEARCH_QUERY"]) == list and type(job["THREAD_FLAIR"]) == list and type(job["LABEL"]) == list:
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
        else:
            return_job.append(
                {
                    "TYPE": _type,
                    "SUBREDDIT": job["SUBREDDIT"],
                    "SEARCH_QUERY": job["SEARCH_QUERY"],
                    "THREAD_FLAIR": job["THREAD_FLAIR"],
                    "LABEL": job["LABEL"]
                }
            )
    return return_job

def parse_jobs(jobs_list):
    list_of_job_args = []
    for job in jobs_list:
        list_of_job_args.append(tuple([job[key] for key in job.keys()]))
    return list_of_job_args

def read_session(
    json_path: str,
    ):
    with open(json_path) as file:
        return json.load(file)

def save_session(
    labels: list,
    jobs: list,
    json_path: str,
    ):
    unpacked_jobs = unpack_jobs(jobs)
    dict_to_save = {"labels": labels, "jobs": unpacked_jobs}
    # json_obj = json.dumps(dict_to_save)
    with open(json_path, 'w') as file:
        json.dump(dict_to_save, file, indent=4)

if __name__ == "__main__":
    WRITE_TO_PATH = "webscraper_session/gotoubun_no_hanayome.json"
    session = read_session(WRITE_TO_PATH)
    labels, jobs = extract_labels_and_jobs_from_session(WRITE_TO_PATH)
    print(labels)
    print(jobs)