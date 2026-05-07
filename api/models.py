from pydantic import BaseModel, model_validator


class CrewMember(BaseModel):
    id: int
    department: str
    job: str
    known_for_department: str
    name: str
    original_name: str
    profile_path: str | None = None


class GuestStar(BaseModel):
    id: int
    character: str
    known_for_department: str
    name: str
    original_name: str
    profile_path: str | None = None


class Episode(BaseModel):
    id: int
    episode_type: str
    episode_number: int
    name: str
    overview: str
    season_number: int
    show_id: int | None = None
    still_path: str | None = None
    vote_average: float
    vote_count: int
    crew: list[CrewMember] | None = None
    guests: list[GuestStar] | None = None


class Season(BaseModel):
    id: int
    episode_count: int
    name: str
    overview: str
    poster_path: str | None = None
    season_number: int
    vote_average: float
    episodes: list[Episode]


class Show(BaseModel):
    id: int
    number_of_episodes: int
    number_of_seasons: int
    origin_country: list[str]
    original_language: str
    original_name: str
    overview: str
    poster_path: str | None = None
    name: str
    vote_average: float
    vote_count: int
    seasons: list[Season]


class SearchResult(BaseModel):
    page: int
    results: list[Show]


class Success[T](BaseModel):
    data: T


class Failure(BaseModel):
    status_code: int
    status_message: str
