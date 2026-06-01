from strands import tool
import requests

@tool
def get_market_discussion(keywords: str,limit: int = 10) -> dict:
    """Fetch market discussion data for the given keywords."""
    try:
        print(f"Fetching discussion data for keyword: {keywords}")
        response = requests.get(
            "https://hn.algolia.com/api/v1/search",
            params={"query": keywords, "hitsPerPage": limit}
        )
        if response.status_code == 200:
            data = response.json()
            discussion_results = []
            for hit in data.get("hits", []):
                discussion_results.append({
                    "title": hit.get("title"),
                    "url": hit.get("url"),
                    "points": hit.get("points"),
                    "created_at": hit.get("created_at"),
                    "author": hit.get("author"),
                    "comments": hit.get("num_comments"),
                    "story_text": hit.get("story_text")
                })
            

            return {
                "status": "success",
                "keyword": keywords,
                "mention_count": len(discussion_results),
                "total_points": sum(
                    item["points"] or 0
                    for item in discussion_results
                ),
                "total_comments": sum(
                    item["comments"] or 0
                    for item in discussion_results
                ),
                "discussion_data": discussion_results,
                "average_points": round(sum(item["points"] or 0 for item in discussion_results) / len(discussion_results), 2) if discussion_results else 0,
                "average_comments": round(sum(item["comments"] or 0 for item in discussion_results) / len(discussion_results), 2) if discussion_results else 0
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to fetch discussion data. Status code: {response.status_code}"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }