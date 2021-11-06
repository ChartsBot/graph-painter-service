from __future__ import annotations

from abc import ABC
from datetime import datetime
from typing import Optional, List, Any
import pydantic


class DataTradePoint(pydantic.BaseModel):
    date: datetime
    volume: Optional[float]

    class Config:
        """Pydantic config class"""
        allow_mutation = False

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.date)

    def __lt__(self, other):
        return self.date < other


class OhclTradePoint(DataTradePoint, pydantic.BaseModel):
    v_open: float
    v_high: float
    v_low: float
    v_close: float

    class Config:
        """Pydantic config class"""
        allow_mutation = False


class SingleTradePoint(DataTradePoint, pydantic.BaseModel):
    value: float

    class Config:
        """Pydantic config class"""
        allow_mutation = False


class AbsCollection(pydantic.BaseModel, ABC):
    coll: List[DataTradePoint]

    def add(self, data_point: DataTradePoint) -> None:
        """Add a new data point to the collection and sort it."""
        self.coll.append(data_point)
        self.coll.sort(key=lambda x: x.date)

    def first_value(self) -> DataTradePoint:
        """Returns the data point with the earliest recorded value"""
        return self.coll[0]

    def last_value(self) -> DataTradePoint:
        """Returns the data point with the latest recorded value"""
        return self.coll[-1]

    def size(self) -> int:
        """Number of elements in the collection"""
        return len(self.coll)

    def total_volume(self) -> Optional[int]:
        """Returns the total volume of the collection"""
        vol = 0
        is_none = True
        for ohcl in self.coll:
            if ohcl.volume is not None:
                is_none = False
                vol += ohcl.volume
        if is_none:
            return False
        else:
            return vol

    def volumes(self) -> List[Optional[float]]:
        """Returns a list containing all the volumes, sorted by time"""
        return [d.volume for d in self.coll]

    def dates(self) -> List[datetime]:
        """Returns a list containing all the dates, sorted by time"""
        return [d.date for d in self.coll]

    def closest_to(self, date_to_compare: datetime) -> DataTradePoint:
        """Returns the datapoint that has the closest date to the given argument"""
        return min(self.coll, key=lambda x: abs(x.date - date_to_compare))

    def matching_date_ts_seconds(self, ts: int) -> Optional[DataTradePoint]:
        """If any, returns a DataTradePoint whose time is matching. Timestamp has to be in seconds"""
        return next(x for x in self.coll if x.date.timestamp() == ts)


# noinspection SpellCheckingInspection
class CollectionSingleTradePoint(AbsCollection, pydantic.BaseModel):
    """Represents a collection of single trade points.
    Adds easy way to access relevant value"""
    coll: Optional[List[SingleTradePoint]] = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.coll is None:
            self.coll = []

    @classmethod
    def from_raw_values(cls, values: List[float], volumes: List[Optional[float]],
                        dates: List[datetime]) -> CollectionSingleTradePoint:
        """Returns an initialized collection from the provided raw value"""
        col = CollectionSingleTradePoint()
        for i in range(len(values)):
            col.add(SingleTradePoint(value=values[i],
                                     volume=volumes[i],
                                     date=dates[i]))
        return col

    def regroup(self, size) -> CollectionSingleTradePoint:
        """Merges the collection of single trade points by groupe of 'size' into a new Collection"""

        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield CollectionOhcl(coll=lst[i:i + n])

        tmp = chunks(self.coll, size)
        new_coll = CollectionSingleTradePoint()
        for colls in tmp:
            earliest = colls.first_value()
            new_ohcl = SingleTradePoint(value=earliest.value,
                                        date=earliest.date,
                                        volume=colls.total_volume())
            new_coll.add(new_ohcl)
        return new_coll

    def values(self) -> List[float]:
        return [d.value for d in self.coll]


# noinspection SpellCheckingInspection
class CollectionOhcl(AbsCollection, pydantic.BaseModel):
    """Represents a collection of Ohcls.
    Adds easy way to access relevant value"""
    coll: Optional[List[OhclTradePoint]] = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.coll is None:
            self.coll = []

    @classmethod
    def from_raw_values(cls, opens: List[float], highs: List[float], lows: List[float], closes: List[float],
                        volumes: List[Optional[float]], dates: List[datetime]) -> CollectionOhcl:
        """Returns an initialized collection from the provided raw value"""
        col = CollectionOhcl()
        for i in range(len(opens)):
            col.add(OhclTradePoint(v_open=opens[i],
                                   v_close=closes[i],
                                   v_low=lows[i],
                                   v_high=highs[i],
                                   volume=volumes[i],
                                   date=dates[i]))
        return col

    def highest_value(self) -> OhclTradePoint:
        """Returns the OHCL with the highest value"""
        return max(self.coll, key=lambda x: x.v_high)

    def lowest_value(self) -> OhclTradePoint:
        """return the OHCL with the lowest value"""
        return min(self.coll, key=lambda x: x.v_low)

    def lows(self) -> List[float]:
        """Returns a list containing all the lows, sorted by time"""
        return [d.v_low for d in self.coll]

    def highs(self) -> List[float]:
        """Returns a list containing all the highs, sorted by time"""
        return [d.v_high for d in self.coll]

    def opens(self) -> List[float]:
        """Returns a list containing all the opens, sorted by time"""
        return [d.v_open for d in self.coll]

    def closes(self) -> List[float]:
        """Returns a list containing all the closes, sorted by time"""
        return [d.v_close for d in self.coll]

    def regroup(self, size) -> CollectionOhcl:
        """Merges the collection of ohcl by groupe of 'size' into a new CollectionOHCL"""

        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield CollectionOhcl(coll=lst[i:i + n])

        tmp = chunks(self.coll, size)
        new_coll = CollectionOhcl()
        for colls in tmp:
            earliest = colls.first_value()
            new_ohcl = OhclTradePoint(v_open=earliest.v_open,
                                      v_close=colls.last_value().v_close,
                                      v_low=colls.lowest_value().v_low,
                                      v_high=colls.highest_value().v_high,
                                      date=earliest.date,
                                      volume=colls.total_volume())
            new_coll.add(new_ohcl)
        return new_coll
