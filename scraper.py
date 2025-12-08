import requests
import pandas as pd
import json
import time

# ----------------------------------
# CONFIG FOR MULTIPLE COMPANIES
# ----------------------------------
COMPANIES = {
    "Walmart": {
        "URL": "https://walmart.wd5.myworkdayjobs.com/wday/cxs/walmart/WalmartExternal/jobs",
        "PRE_URL": "https://walmart.wd5.myworkdayjobs.com/en-US/WalmartExternal",
        "payloadFilters": {}
    },

    "Target": {
        "URL": "https://target.wd5.myworkdayjobs.com/wday/cxs/target/targetcareers/jobs",
        "PRE_URL": "https://target.wd5.myworkdayjobs.com/en-US/targetcareers",
        "payloadFilters": {}
    },

    "Adobe": {
        "URL": "https://adobe.wd5.myworkdayjobs.com/wday/cxs/adobe/external_experienced/jobs",
        "PRE_URL": "https://adobe.wd5.myworkdayjobs.com/en-US/external_experienced",
        "payloadFilters": {}
    }
}

# Search keywords
SEARCH_TERMS = [
    "data scientist",
    "data analyst",
    "business intelligence",
    "ai engineer",
    "ml engineer",
    "business analyst"
]

# Workday CxS headers
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive"
}

# ----------------------------------------------------------
# FUNCTION: FETCH ALL JOBS FOR ONE COMPANY & ONE SEARCH TERM
# ----------------------------------------------------------
def fetch_jobs_for_company(company, config, search_text):
    all_jobs = []
    offset = 0
    limit = 20   # Workday Limit (cannot be  > 20)
    total = 0  
    
    while True:
        payload = {
            "appliedFacets": config.get("payloadFilters", {}),
            "limit": limit,
            "offset": offset,
            "searchText": search_text.replace(" ", "+")
        }

        try:
            response = requests.post(config["URL"], headers=HEADERS, data=json.dumps(payload))
            data = response.json()

            jobs = data.get("jobPostings", [])
            if offset == 0:
                total = data.get("total", 0)
                print("Total Jobs Found : ",total)
            
            if not jobs:
                break  # no more pages

            for job in jobs:
                title = job.get("title", {}) #.get("label", "")
                job_id = job.get("bulletFields", [None])[0]
                external_path = job.get("externalPath", "")
                locations = job.get("locationsText", "")
                #", ".join([loc.get("label", "") for loc in job.get("locations", [])])
                posted_on = job.get("postedOn", "")

                full_url = f"{config['PRE_URL']}{external_path}"

                all_jobs.append({
                    "Company": company,
                    "Search Term": search_text,
                    "Title": title,
                    "Job ID": job_id,
                    "Location": locations,
                    "Posted On": posted_on,
                    "Job URL": full_url
                })

            
            
            # Stop if we already fetched all available jobs
            offset += limit

            current = total if offset >= total else offset
            print("Fetched : ", current , " OF " , total)
            
            if offset >= total:
                break
                
            time.sleep(0.5)  # avoid blocking

        except Exception as e:
            print(f"Error fetching {company} ({search_text}):", e)
            break

    return all_jobs


# ----------------------------------
# MAIN SCRAPER - ALL COMPANIES
# ----------------------------------
final_results = []

for company, config in COMPANIES.items():
    print(f"\n Fetching jobs for: {company}")

    for term in SEARCH_TERMS:
        print(f" Searching: {term} ...")
        jobs = fetch_jobs_for_company(company, config, term)
        final_results.extend(jobs)


# ----------------------------------
# SAVE TO CSV
# ----------------------------------
df = pd.DataFrame(final_results)
df.to_csv("all_jobs.csv", index=False)

print("\n Completed! Saved jobs → all_jobs.csv")
print(f"Total Jobs Collected: {len(df)}")

#PREVENT EMPTY CSV FILE
if len(final_results) == 0:
    print("No jobs scraped, CSV not updated.")
    exit(1)
