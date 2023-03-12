from typing import Optional, Any, List, Dict

from pydantic import BaseModel, Field


class CreateMatchSchema(BaseModel):
    max_rounds: int
    map: str
    team1_roster: List[str]
    team1_name: str
    team2_roster: List[str]
    team2_name: str


class CreatedServerSchema(BaseModel):
    id_: str
    host: str


class MatchDataSchema(BaseModel):
    match_id: str
    server_id: str
    server_host: str
    max_rounds: str
    map: str
    team1_roster: List[str]
    team1_name: str
    team1_score: int
    team2_roster: List[str]
    team2_name: str
    team2_score: int


class CreateMatchResponseSchema(BaseModel):
    status: str = 'OK'
    error: Optional[str]
    match: Optional[MatchDataSchema]


class MatchDathostSchema(BaseModel):
    id_: str = Field(alias='id')
    server_id: str = Field(alias='game_server_id')
    selected_map: str = Field(alias='map')
    connect_time: int
    warmup_time: int

    team1_start_ct: bool
    team1_steam_ids: Optional[List[str]] = Field(alias='team1_roster')
    team1_coach_steam_id: Optional[List[str]] = Field(alias='team1_coaches')
    team1_name: str
    team1_flag: str

    team2_start_ct: bool
    team2_steam_ids: Optional[List[str]] = Field(alias='team1_roster')
    team2_coach_steam_id: Optional[List[str]] = Field(alias='team1_coaches')
    team2_name: str
    team2_flag: str

    spectator_steam_ids: List[str]
    wait_for_coaches: bool
    wait_for_spectators: bool
    round_end_webhook_url: str
    match_end_webhook_url: bool
    started: bool
    finished: bool
    cancel_reason: Optional[str]
    rounds_played: int

    team1_stats: Dict[str, int]
    team2_stats: Dict[str, int]
    player_stats: Dict[str, Any]

    enable_knife_round: bool
    enable_pause: bool
    enable_playwin: bool

    playwin_result_webhook_url: Optional[str]
    playwin_result: Dict[str, Any]

    enable_pause: bool
    ready_min_players: int
    enable_tech_pause: bool
    message_prefix: str