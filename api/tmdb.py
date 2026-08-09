from dotenv import load_dotenv
import httpx
import os
from pydantic import BaseModel, ValidationError
from . import models
from . import schemas
from dataclasses import dataclass
from typing import Any

load_dotenv()


class TmdbException(Exception):
    def __init__(self, status_code: int, status_message: str) -> None:
        self.status_code = status_code
        self.status_message = status_message


class Tmdb:
    def __init__(self) -> None:
        self.api_key = os.getenv("api_key")
        self.api_access_token = os.getenv("api_access_token")
        self.base_url = "https://api.themoviedb.org/3"

    def get[T: BaseModel](
        self,
        endpoint: str,
        model: type[T],
        params: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
    ) -> T:
        if not headers:
            headers = {}
        if not params:
            params = {}
        headers["accept"] = "application/json"
        if not self.api_access_token:
            raise TmdbException(
                status_code=500,
                status_message="invalid creds when trying to make a request",
            )
        headers["Authorization"] = "Bearer " + self.api_access_token
        res = httpx.get(self.base_url + endpoint, params=params, headers=headers)
        res_json = res.json()
        if not res.is_success:
            try:
                fail = schemas.Failure.model_validate(res_json)
                raise TmdbException(
                    status_code=fail.status_code, status_message=fail.status_message
                )
            except ValidationError:
                raise TmdbException(
                    status_code=500,
                    status_message="wtf is that, supposed to be an error but not error",
                )
        try:
            data = model.model_validate(res_json)
            return data
        except ValidationError as e:
            raise TmdbException(status_code=500, status_message=str(e))

    def search_for_show(self, query: str) -> schemas.SearchResults:
        return self.get(
            "/search/tv", params={"query": query}, model=schemas.SearchResults
        )

    def get_show_details(self, series_id: int) -> schemas.Show:
        return self.get(f"/tv/{series_id}", model=schemas.Show)

    def get_season_details(self, series_id: int, season_number: int) -> schemas.Season:
        return self.get(f"/tv/{series_id}/season/{season_number}", model=schemas.Season)

    def get_episode_details(
        self, series_id: int, season_number: int, episode_number: int
    ) -> schemas.Episode:
        return self.get(
            f"/tv/{series_id}/season/{season_number}/episode/{episode_number}",
            model=schemas.Episode,
        )


tmdb_client = Tmdb()
