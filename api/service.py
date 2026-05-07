from dotenv import load_dotenv
import httpx
import os
from pydantic import BaseModel
from models import (
    SearchResult,
    Show,
    Season,
    Episode,
    CrewMember,
    GuestStar,
    Failure,
    Success,
)

load_dotenv()


class Api:
    def __init__(self):
        self.api_key = os.getenv("api_key")
        self.api_access_token = os.getenv("api_access_token")
        self.base_url = "https://api.themoviedb.org/3"

    def get[T: BaseModel](
        self,
        endpoint: str,
        model: T,
        params: dict[str, str] = {},
        headers: dict[str, str] = {},
    ) -> Success | Failure:
        headers["accept"] = "application/json"
        headers["Authorization"] = "Bearer " + self.api_access_token
        res = httpx.get(self.base_url + endpoint, params=params, headers=headers)
        json = res.json()
        if not res.is_success:
            return Failure(
                status_code=json["status_code"], status_message=json["status_message"]
            )
        return Success(data=model.model_validate(json))

    def search_for_show(self, query: str) -> Success[SearchResult] | Failure:
        return self.get("/search/tv", params={"query": query}, model=SearchResult)

    def get_show_details(self, series_id: int) -> Success[Show] | Failure:
        return self.get(f"/tv/{series_id}", model=Show)

    def get_season_details(
        self, series_id: int, season_number: int
    ) -> Success[Season] | Failure:
        return self.get(f"/tv/{series_id}/season/{season_number}", model=Season)

    def get_episode_details(
        self, series_id: int, season_number: int, episode_number: int
    ) -> Success[Episode] | Failure:
        return self.get(
            f"/tv/{series_id}/season/{season_number}/episode/{episode_number}",
            model=Episode,
        )


api = Api()
print(api.get_episode_details(2, 1, 1))
